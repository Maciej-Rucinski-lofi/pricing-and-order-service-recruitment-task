# Copies Graftcode Gateway (gg.exe) into the project so it can write Binaries.zip
# without Program Files permission errors.

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path $PSScriptRoot -Parent

$DestDir = Join-Path $ProjectRoot "tools\graftcode-gateway"
$DestExe = Join-Path $DestDir "gg.exe"
$SourceExe = "C:\Program Files\Graftcode\GraftcodeGateway\bin\gg.exe"

New-Item -ItemType Directory -Force -Path $DestDir | Out-Null

if (Test-Path $DestExe) {
    Write-Host "gg.exe already present at $DestExe"
    exit 0
}

if (-not (Test-Path $SourceExe)) {
    Write-Error @"
gg.exe not found at $SourceExe
Install Graftcode Gateway from https://graftcode.com or https://github.com/grft-dev/graftcode-gateway/releases
"@
}

Write-Host "Copying gg.exe to $DestDir ..."
Copy-Item $SourceExe $DestExe -Force
Write-Host "Done. Run gateway from: $DestDir"
