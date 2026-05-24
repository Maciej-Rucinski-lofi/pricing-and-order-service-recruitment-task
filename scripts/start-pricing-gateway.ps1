$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path $PSScriptRoot -Parent
$GatewayDir = Join-Path $ProjectRoot "tools\graftcode-gateway"
$GgExe = Join-Path $GatewayDir "gg.exe"

. (Join-Path $PSScriptRoot "load-env.ps1") -EnvFile (Join-Path $ProjectRoot ".env")

if (-not (Test-Path $GgExe)) {
    & (Join-Path $PSScriptRoot "setup-gateway.ps1")
}

if (-not $env:PROJECT_KEY -or $env:PROJECT_KEY -eq "your_project_key_here") {
    Write-Error "Set PROJECT_KEY in .env (from https://portal.graftcode.com)."
}

$wsPort = if ($env:PRICING_GATEWAY_WS_PORT) { $env:PRICING_GATEWAY_WS_PORT } else { "9080" }
$httpPort = if ($env:PRICING_GATEWAY_HTTP_PORT) { $env:PRICING_GATEWAY_HTTP_PORT } else { "9081" }

$VenvScripts = Join-Path $ProjectRoot ".venv\Scripts"
$PythonExe = Join-Path $VenvScripts "python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Error "Missing $PythonExe - run: python -m venv .venv; pip install -e `".[dev]`""
}

# python3 alias for Graftcode Python launcher
$Python3Exe = Join-Path $VenvScripts "python3.exe"
if (-not (Test-Path $Python3Exe)) {
    Copy-Item $PythonExe $Python3Exe
}

# Resolve a system Python 3 (Graftcode needs an interpreter outside the Store shim)
$SystemPythonDir = $null
try {
    $pyLines = & py -3.12 -c "import sys, os; print(os.path.dirname(sys.executable))" 2>$null
    if ($pyLines) { $SystemPythonDir = $pyLines.Trim() }
} catch { }

$pathParts = @($VenvScripts)
if ($SystemPythonDir -and (Test-Path $SystemPythonDir)) {
    $pathParts += $SystemPythonDir
}
$pathParts += ($env:PATH -split ';' | Where-Object {
    $_ -and $_ -notmatch 'WindowsApps\\python'
})
$env:PATH = ($pathParts -join ';')
$env:PYTHONPATH = $ProjectRoot

Write-Host "Starting Pricing Gateway..."
Write-Host "  Python:   $PythonExe"
Write-Host "  modules:  $ProjectRoot (PricingGateway.calculate_price)"
Write-Host "  Vision:   http://localhost:${httpPort}/GV"
Write-Host "  WebSocket port: $wsPort"

Set-Location $GatewayDir
& $GgExe `
    --projectKey $env:PROJECT_KEY `
    --runtime python `
    --modules $ProjectRoot `
    --types pricing_service.gateway_host.PricingGateway `
    --port $wsPort `
    --httpPort $httpPort
