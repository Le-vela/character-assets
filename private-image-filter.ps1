param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("Clean", "Smudge")]
    [string]$Mode
)

$ErrorActionPreference = "Stop"

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

function Read-StandardInputBytes {
    $stream = [Console]::OpenStandardInput()
    $memory = [IO.MemoryStream]::new()
    try {
        $buffer = New-Object byte[] 8192
        while (($read = $stream.Read($buffer, 0, $buffer.Length)) -gt 0) {
            $memory.Write($buffer, 0, $read)
        }

        $memory.ToArray()
    }
    finally {
        $memory.Dispose()
    }
}

function Write-StandardOutputBytes {
    param([byte[]]$Bytes)

    $stream = [Console]::OpenStandardOutput()
    $stream.Write($Bytes, 0, $Bytes.Length)
    $stream.Flush()
}

function Protect-Bytes {
    param(
        [byte[]]$PlainBytes,
        [string]$Password
    )

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
            $cipherBytes = $encryptor.TransformFinalBlock($PlainBytes, 0, $PlainBytes.Length)
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
    $outBytes
}

function Unprotect-Bytes {
    param(
        [byte[]]$InputBytes,
        [string]$Password
    )

    $magic = [Text.Encoding]::ASCII.GetBytes("PIMG1")
    $minimumLength = $magic.Length + 16 + 16 + 32 + 1
    if ($InputBytes.Length -lt $minimumLength) {
        return $InputBytes
    }

    for ($i = 0; $i -lt $magic.Length; $i++) {
        if ($InputBytes[$i] -ne $magic[$i]) {
            return $InputBytes
        }
    }

    $tagOffset = $InputBytes.Length - 32
    $payload = New-Object byte[] $tagOffset
    $expectedTag = New-Object byte[] 32
    [Array]::Copy($InputBytes, 0, $payload, 0, $payload.Length)
    [Array]::Copy($InputBytes, $tagOffset, $expectedTag, 0, 32)

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
        throw "PRIVATE_IMAGE_PASSWORD is incorrect or the file was modified."
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
            $decryptor.TransformFinalBlock($cipherBytes, 0, $cipherBytes.Length)
        }
        finally {
            $decryptor.Dispose()
        }
    }
    finally {
        $aes.Dispose()
    }
}

$password = $env:PRIVATE_IMAGE_PASSWORD
if ([string]::IsNullOrWhiteSpace($password)) {
    throw "Set PRIVATE_IMAGE_PASSWORD before using the private image Git filter."
}

$inputBytes = Read-StandardInputBytes
if ($Mode -eq "Clean") {
    Write-StandardOutputBytes -Bytes (Protect-Bytes -PlainBytes $inputBytes -Password $password)
}
else {
    Write-StandardOutputBytes -Bytes (Unprotect-Bytes -InputBytes $inputBytes -Password $password)
}
