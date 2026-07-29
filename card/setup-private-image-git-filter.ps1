param(
    [string]$ListPath = "private-images.txt"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $ListPath)) {
    throw "List file not found: $ListPath"
}

$repoRoot = (& git rev-parse --show-toplevel).Trim()
if ([string]::IsNullOrWhiteSpace($repoRoot)) {
    throw "This script must be run inside a Git repository."
}

$filterScript = Join-Path $repoRoot "private-image-filter.ps1"
if (-not (Test-Path -LiteralPath $filterScript)) {
    throw "Filter script not found: $filterScript"
}

$names = foreach ($line in Get-Content -LiteralPath $ListPath) {
    $trimmed = $line.Trim()
    if ($trimmed.Length -eq 0 -or $trimmed.StartsWith("#")) {
        continue
    }

    [IO.Path]::GetFileName($trimmed)
}

if (-not $names -or $names.Count -eq 0) {
    throw "No file names were found in $ListPath"
}

$attributesPath = Join-Path $repoRoot ".gitattributes"
$existing = @()
if (Test-Path -LiteralPath $attributesPath) {
    $existing = Get-Content -LiteralPath $attributesPath
}

$generatedStart = "# private-image-filter:start"
$generatedEnd = "# private-image-filter:end"
$kept = New-Object 'System.Collections.Generic.List[string]'
$insideGenerated = $false
foreach ($line in $existing) {
    if ($line -eq $generatedStart) {
        $insideGenerated = $true
        continue
    }
    if ($line -eq $generatedEnd) {
        $insideGenerated = $false
        continue
    }
    if (-not $insideGenerated) {
        $kept.Add($line)
    }
}

$generated = New-Object 'System.Collections.Generic.List[string]'
$generated.Add($generatedStart)
foreach ($name in $names) {
    $escaped = $name.Replace("[", "\[").Replace("]", "\]")
    $generated.Add("**/$escaped filter=private-image -diff -merge")
}
$generated.Add($generatedEnd)

$newContent = @($kept | Where-Object { $_ -ne "" }) + @("") + $generated
Set-Content -LiteralPath $attributesPath -Value $newContent -Encoding ASCII

$cleanCommand = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$filterScript`" -Mode Clean"
$smudgeCommand = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$filterScript`" -Mode Smudge"

& git config --local filter.private-image.clean $cleanCommand
& git config --local filter.private-image.smudge $smudgeCommand
& git config --local filter.private-image.required true

Write-Host "Updated .gitattributes and local Git filter config."
Write-Host "Set PRIVATE_IMAGE_PASSWORD before git add/commit/checkout."
Write-Host "To encrypt already tracked files in the Git index, run:"
Write-Host "  git add --renormalize ."
