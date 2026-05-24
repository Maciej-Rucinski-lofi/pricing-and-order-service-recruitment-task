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

$wsPort = if ($env:ORDER_GATEWAY_WS_PORT) { $env:ORDER_GATEWAY_WS_PORT } else { "9082" }
$httpPort = if ($env:ORDER_GATEWAY_HTTP_PORT) { $env:ORDER_GATEWAY_HTTP_PORT } else { "9083" }
$pricingMode = if ($env:PRICING_MODE) { $env:PRICING_MODE } else { "LOCAL" }

$VenvScripts = Join-Path $ProjectRoot ".venv\Scripts"
$PythonExe = Join-Path $VenvScripts "python.exe"
if (-not (Test-Path $PythonExe)) {
    Write-Error "Missing $PythonExe - run: python -m venv .venv; pip install -e `".[dev]`""
}

$Python3Exe = Join-Path $VenvScripts "python3.exe"
if (-not (Test-Path $Python3Exe)) {
    Copy-Item $PythonExe $Python3Exe
}

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
$env:PRICING_MODE = $pricingMode

Write-Host "Starting Order Gateway (PRICING_MODE=$pricingMode)..."
Write-Host "  Vision: http://localhost:${httpPort}/GV"
Write-Host "  WebSocket port: $wsPort"

Set-Location $GatewayDir
& $GgExe `
    --projectKey $env:PROJECT_KEY `
    --runtime python `
    --modules $ProjectRoot `
    --types order_service.gateway_host.OrderGateway `
    --port $wsPort `
    --httpPort $httpPort
