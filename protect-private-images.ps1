param(
    [ValidateSet("Encrypt", "Decrypt")]
    [string]$Mode = "Encrypt",

    [string]$ListPath = "private-images.txt",

    [string]$RootPath = ".",

    [switch]$RemoveOriginal
)

$ErrorActionPreference = "Stop"

function Get-PlainTextFromSecureString {
    param([securestring]$SecureString)

    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureString)
    try {
        [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

function Get-PrivateNames {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        throw "List file not found: $Path"
    }

    $names = New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
    foreach ($line in Get-Content -LiteralPath $Path) {
        $trimmed = $line.Trim()
        if ($trimmed.Length -eq 0 -or $trimmed.StartsWith("#")) {
            continue
        }

        [void]$names.Add([IO.Path]::GetFileName($trimmed))
    }

    if ($names.Count -eq 0) {
        throw "No file names were found in $Path"
    }

    $names
}

function Get-Keys {
    param(
        [string]$Password,
        [byte[]]$Salt
    )

    $derive = [Security.Cryptography.Rfc2898DeriveBytes]::new(
        $Password,
        $Salt,
        210000,
        [Security.Cryptography.HashAlgorithmName]::SHA256
    )
    try {
        @{
            AesKey = $derive.GetBytes(32)
            MacKey = $derive.GetBytes(32)
        }
    }
    finally {
        $derive.Dispose()
    }
}

function Fill-RandomBytes {
    param([byte[]]$Bytes)

    $rng = [Security.Cryptography.RNGCryptoServiceProvider]::new()
    try {
        $rng.GetBytes($Bytes)
    }
    finally {
        $rng.Dispose()
    }
}

function Test-FixedTimeEquals {
    param(
        [byte[]]$Left,
        [byte[]]$Right
    )

    if ($Left.Length -ne $Right.Length) {
        return $false
    }

    $diff = 0
    for ($i = 0; $i -lt $Left.Length; $i++) {
        $diff = $diff -bor ($Left[$i] -bxor $Right[$i])
    }

    $diff -eq 0
}

function Protect-File {
    param(
        [string]$Path,
        [string]$Password
    )

    $plainBytes = [IO.File]::ReadAllBytes($Path)
    $salt = New-Object byte[] 16
    $iv = New-Object byte[] 16
    Fill-RandomBytes -Bytes $salt
    Fill-RandomBytes -Bytes $iv
    $keys = Get-Keys -Password $Password -Salt $salt

    $aes = [Security.Cryptography.Aes]::Create()
    try {
        $aes.KeySize = 256
        $aes.Mode = [Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [Security.Cryptography.PaddingMode]::PKCS7
        $aes.Key = $keys.AesKey
        $aes.IV = $iv

        $encryptor = $aes.CreateEncryptor()
        try {
            $cipherBytes = $encryptor.TransformFinalBlock($plainBytes, 0, $plainBytes.Length)
        }
        finally {
            $encryptor.Dispose()
        }
    }
    finally {
        $aes.Dispose()
    }

    $magic = [Text.Encoding]::ASCII.GetBytes("PIMG1")
    $payload = New-Object byte[] ($magic.Length + $salt.Length + $iv.Length + $cipherBytes.Length)
    [Array]::Copy($magic, 0, $payload, 0, $magic.Length)
    [Array]::Copy($salt, 0, $payload, $magic.Length, $salt.Length)
    [Array]::Copy($iv, 0, $payload, $magic.Length + $salt.Length, $iv.Length)
    [Array]::Copy($cipherBytes, 0, $payload, $magic.Length + $salt.Length + $iv.Length, $cipherBytes.Length)

    $hmac = [Security.Cryptography.HMACSHA256]::new($keys.MacKey)
    try {
        $tag = $hmac.ComputeHash($payload)
    }
    finally {
        $hmac.Dispose()
    }

    $outBytes = New-Object byte[] ($payload.Length + $tag.Length)
    [Array]::Copy($payload, 0, $outBytes, 0, $payload.Length)
    [Array]::Copy($tag, 0, $outBytes, $payload.Length, $tag.Length)

    $outputPath = "$Path.enc"
    [IO.File]::WriteAllBytes($outputPath, $outBytes)
    $outputPath
}

function Unprotect-File {
    param(
        [string]$Path,
        [string]$Password
    )

    $inputBytes = [IO.File]::ReadAllBytes($Path)
    $magic = [Text.Encoding]::ASCII.GetBytes("PIMG1")
    $minimumLength = $magic.Length + 16 + 16 + 32 + 1
    if ($inputBytes.Length -lt $minimumLength) {
        throw "Encrypted file is too small or invalid: $Path"
    }

    for ($i = 0; $i -lt $magic.Length; $i++) {
        if ($inputBytes[$i] -ne $magic[$i]) {
            throw "Encrypted file has an invalid header: $Path"
        }
    }

    $tagOffset = $inputBytes.Length - 32
    $payload = New-Object byte[] $tagOffset
    $expectedTag = New-Object byte[] 32
    [Array]::Copy($inputBytes, 0, $payload, 0, $payload.Length)
    [Array]::Copy($inputBytes, $tagOffset, $expectedTag, 0, 32)

    $salt = New-Object byte[] 16
    $iv = New-Object byte[] 16
    [Array]::Copy($payload, $magic.Length, $salt, 0, 16)
    [Array]::Copy($payload, $magic.Length + 16, $iv, 0, 16)
    $keys = Get-Keys -Password $Password -Salt $salt

    $hmac = [Security.Cryptography.HMACSHA256]::new($keys.MacKey)
    try {
        $actualTag = $hmac.ComputeHash($payload)
    }
    finally {
        $hmac.Dispose()
    }

    if (-not (Test-FixedTimeEquals -Left $actualTag -Right $expectedTag)) {
        throw "Password is incorrect or the file was modified: $Path"
    }

    $cipherOffset = $magic.Length + 16 + 16
    $cipherBytes = New-Object byte[] ($payload.Length - $cipherOffset)
    [Array]::Copy($payload, $cipherOffset, $cipherBytes, 0, $cipherBytes.Length)

    $aes = [Security.Cryptography.Aes]::Create()
    try {
        $aes.KeySize = 256
        $aes.Mode = [Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [Security.Cryptography.PaddingMode]::PKCS7
        $aes.Key = $keys.AesKey
        $aes.IV = $iv

        $decryptor = $aes.CreateDecryptor()
        try {
            $plainBytes = $decryptor.TransformFinalBlock($cipherBytes, 0, $cipherBytes.Length)
        }
        finally {
            $decryptor.Dispose()
        }
    }
    finally {
        $aes.Dispose()
    }

    $outputPath = $Path -replace '\.enc$', ''
    if ($outputPath -eq $Path) {
        $outputPath = "$Path.dec"
    }

    [IO.File]::WriteAllBytes($outputPath, $plainBytes)
    $outputPath
}

$root = Resolve-Path -LiteralPath $RootPath
$names = Get-PrivateNames -Path $ListPath
$password = $env:PRIVATE_IMAGE_PASSWORD
if ([string]::IsNullOrEmpty($password)) {
    $password = Get-PlainTextFromSecureString -SecureString (Read-Host "Password" -AsSecureString)
}
if ([string]::IsNullOrWhiteSpace($password)) {
    throw "Password cannot be empty."
}

if ($Mode -eq "Encrypt") {
    $matches = Get-ChildItem -LiteralPath $root -Recurse -File |
        Where-Object { $names.Contains($_.Name) -and -not $_.Name.EndsWith(".enc", [StringComparison]::OrdinalIgnoreCase) }

    foreach ($file in $matches) {
        $encryptedPath = Protect-File -Path $file.FullName -Password $password
        Write-Host "Encrypted: $($file.FullName) -> $encryptedPath"
        if ($RemoveOriginal) {
            Remove-Item -LiteralPath $file.FullName -Force
            Write-Host "Removed original: $($file.FullName)"
        }
    }
}
else {
    $encryptedNames = foreach ($name in $names) {
        if ($name.EndsWith(".enc", [StringComparison]::OrdinalIgnoreCase)) {
            $name
        }
        else {
            "$name.enc"
        }
    }

    $matches = Get-ChildItem -LiteralPath $root -Recurse -File |
        Where-Object { $encryptedNames -contains $_.Name }

    foreach ($file in $matches) {
        $decryptedPath = Unprotect-File -Path $file.FullName -Password $password
        Write-Host "Decrypted: $($file.FullName) -> $decryptedPath"
        if ($RemoveOriginal) {
            Remove-Item -LiteralPath $file.FullName -Force
            Write-Host "Removed encrypted file: $($file.FullName)"
        }
    }
}

if (-not $matches -or $matches.Count -eq 0) {
    Write-Warning "No matching files were found under $root."
}
