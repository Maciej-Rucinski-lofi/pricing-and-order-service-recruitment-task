param(
    # Force image rebuild (only needed after Dockerfile / gg version changes)
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
    Write-Host ""
    Write-Host "Docker is not running." -ForegroundColor Red
    Write-Host "  Start Docker Desktop, then run: .\scripts\start-pricing-gateway-docker.ps1"
    Write-Host ""
    exit 1
}

$image = "pricing-gateway:local"
$wsPort = if ($env:PRICING_GATEWAY_WS_PORT) { $env:PRICING_GATEWAY_WS_PORT } else { "9080" }
$httpPort = if ($env:PRICING_GATEWAY_HTTP_PORT) { $env:PRICING_GATEWAY_HTTP_PORT } else { "9081" }

if ($Build -or -not (Test-DockerImage $image)) {
    Write-Host "Building $image (one-time; use -Build to rebuild after Dockerfile changes) ..."
    docker build -f (Join-Path $ProjectRoot "Dockerfile.pricing-gateway") -t $image $ProjectRoot
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
} else {
    Write-Host "Using existing image $image (rebuild with -Build if needed)."
}

Write-Host "Starting container with live code mount: $ProjectRoot -> /app"
Write-Host "Vision: http://localhost:${httpPort}/GV"
Write-Host "After Python edits: stop (Ctrl+C) and run this script again - no rebuild required."
Write-Host ""

docker run --rm -it `
    -v "${ProjectRoot}:/app" `
    -e "PROJECT_KEY=$env:PROJECT_KEY" `
    -p "${wsPort}:9080" `
    -p "${httpPort}:9081" `
    $image
