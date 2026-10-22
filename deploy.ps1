# Build and deploy the Task Manager to Cloud Run.
#
#   .\deploy.ps1                 # api (with migrations) + frontend
#   .\deploy.ps1 -SkipFrontend   # backend only
#   .\deploy.ps1 -SkipApi        # frontend only
#
# Only the image changes on each deploy; everything else (service account,
# Cloud SQL socket, secrets, CORS_ORIGINS) stays as configured in Steps 4-7.
# If scripts are blocked: powershell -ExecutionPolicy Bypass -File .\deploy.ps1

param(
    [string]$Tag,
    [switch]$SkipApi,
    [switch]$SkipFrontend
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Project  = "taskmanagrger"
$Region   = "europe-west1"
$Registry = "$Region-docker.pkg.dev/$Project/taskmanager"

# Tag images with the git commit so every revision maps back to the code it runs.
if (-not $Tag) {
    $Tag = git rev-parse --short HEAD
    if (git status --porcelain) {
        # Uncommitted changes: the commit alone doesn't describe this build.
        $Tag = "$Tag-dirty-$(Get-Date -Format 'yyyyMMddHHmm')"
    }
}

function Invoke-Step([string]$Name, [scriptblock]$Command) {
    Write-Host "`n==> $Name" -ForegroundColor Cyan
    & $Command
    if ($LASTEXITCODE -ne 0) { throw "$Name failed (exit code $LASTEXITCODE)" }
}

if (-not $SkipApi) {
    $ApiImage = "$Registry/api:$Tag"

    Invoke-Step "Build api image ($Tag)" {
        gcloud builds submit backend --tag=$ApiImage --project=$Project
    }
    # Migrate before deploying, so the new code never runs against an old schema.
    Invoke-Step "Point migrate job at new image" {
        gcloud run jobs update migrate --image=$ApiImage --region=$Region --project=$Project
    }
    Invoke-Step "Run migrations" {
        gcloud run jobs execute migrate --region=$Region --project=$Project --wait
    }
    Invoke-Step "Deploy api" {
        gcloud run deploy api --image=$ApiImage --region=$Region --project=$Project
    }
}

if (-not $SkipFrontend) {
    $FrontendImage = "$Registry/frontend:$Tag"
    $ApiUrl = gcloud run services describe api --region=$Region --project=$Project --format="value(status.url)"

    # VITE_API_URL is baked into the bundle at build time.
    Invoke-Step "Build frontend image ($Tag, API $ApiUrl)" {
        gcloud builds submit frontend --config=frontend/cloudbuild.yaml --project=$Project `
            --substitutions="_VITE_API_URL=$ApiUrl,_IMAGE=$FrontendImage"
    }
    Invoke-Step "Deploy frontend" {
        gcloud run deploy frontend --image=$FrontendImage --region=$Region --project=$Project
    }
}

Write-Host "`nDeployed $Tag" -ForegroundColor Green
gcloud run services list --project=$Project --format="table(metadata.name,status.url)"
