# Phase 0 prerequisite checks

$ErrorActionPreference = "Continue"
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$allOk = $true

function Check {
    param(
        [string]$Name,
        [bool]$Pass,
        [string]$Detail
    )
    $symbol = if ($Pass) { "[OK]" } else { "[FAIL]" }
    Write-Host "$symbol $Name - $Detail"
    if (-not $Pass) { $script:allOk = $false }
}

$pyVersion = & python --version 2>&1 | Out-String
$pyOk = $pyVersion -match "Python 3\.(1[1-9]|[2-9][0-9])"
Check "Python 3.11+" $pyOk $pyVersion.Trim()

$venvPy = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
Check "Virtualenv" (Test-Path $venvPy) $venvPy

try {
    $dockerVersion = (& docker --version 2>&1 | Out-String).Trim()
    Check "Docker" $true $dockerVersion
} catch {
    Check "Docker" $false "docker not found"
}

$ggExe = Join-Path $ProjectRoot "tools\graftcode-gateway\gg.exe"
Check "Gateway (project copy)" (Test-Path $ggExe) $ggExe

$binariesZip = Join-Path $ProjectRoot "tools\graftcode-gateway\Binaries.zip"
Check "Binaries.zip" (Test-Path $binariesZip) "Created when gg runs from tools/graftcode-gateway"

$envExample = Join-Path $ProjectRoot ".env.example"
Check ".env.example" (Test-Path $envExample) $envExample

$envFile = Join-Path $ProjectRoot ".env"
if (Test-Path $envFile) {
    Check ".env file" $true "Present (set PROJECT_KEY from portal)"
} else {
    Write-Host "[WARN] .env - copy .env.example to .env and set PROJECT_KEY"
}

if (-not $allOk) { exit 1 }
Write-Host ""
Write-Host "Phase 0 checks passed."
