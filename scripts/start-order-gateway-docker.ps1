param(
    [switch]$Build
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path $PSScriptRoot -Parent

. (Join-Path $PSScriptRoot "load-env.ps1") -EnvFile (Join-Path $ProjectRoot ".env")

function Test-DockerDaemon {
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & docker info *> $null
        return $LASTEXITCODE -eq 0
    } finally {
        $ErrorActionPreference = $previousPreference
    }
}

function Test-DockerImage {
    param([string]$Name)
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        & docker image inspect $Name *> $null
        return $LASTEXITCODE -eq 0
    } finally {
        $ErrorActionPreference = $previousPreference
    }
}

if (-not (Test-DockerDaemon)) {
    Write-Host "Docker is not running. Start Docker Desktop and retry." -ForegroundColor Red
    exit 1
}

$image = "order-gateway:local"
$wsPort = if ($env:ORDER_GATEWAY_WS_PORT) { $env:ORDER_GATEWAY_WS_PORT } else { "9082" }
$httpPort = if ($env:ORDER_GATEWAY_HTTP_PORT) { $env:ORDER_GATEWAY_HTTP_PORT } else { "9083" }
$pricingMode = if ($env:PRICING_MODE) { $env:PRICING_MODE } else { "LOCAL" }

if ($Build -or -not (Test-DockerImage $image)) {
    Write-Host "Building $image ..."
    docker build -f (Join-Path $ProjectRoot "Dockerfile.order-gateway") -t $image $ProjectRoot
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    Write-Host "Using existing image $image (rebuild with -Build if needed)."
}

Write-Host "Starting Order Gateway (PRICING_MODE=$pricingMode)"
Write-Host "  Vision: http://localhost:${httpPort}/GV"
Write-Host "  Try: place_order('laptop', 1, 'regular')"
Write-Host "  Python edits: restart only. First start ~30s (gg init). Rebuild (-Build) after dependency changes."
Write-Host ""

docker run --rm -it `
    -v "${ProjectRoot}:/app" `
    -e "PROJECT_KEY=$env:PROJECT_KEY" `
    -e "PRICING_MODE=$pricingMode" `
    -e "GRAFT_CONFIG=$env:GRAFT_CONFIG" `
    -e "GRAFT_PACKAGE_MODULE=$env:GRAFT_PACKAGE_MODULE" `
    -p "${wsPort}:9082" `
    -p "${httpPort}:9083" `
    $image
