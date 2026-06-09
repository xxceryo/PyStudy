[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$frontendRoot = Join-Path $projectRoot "frontend"
$jobs = @()

function Assert-Command {
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found in PATH."
    }
}

function Receive-ServiceOutput {
    param(
        [Parameter(Mandatory)]
        [System.Management.Automation.Job[]]$ServiceJobs
    )

    foreach ($serviceJob in $ServiceJobs) {
        Receive-Job -Job $serviceJob
    }
}

try {
    Assert-Command -Name "uv"
    Assert-Command -Name "npm"

    $envPath = Join-Path $projectRoot ".env"
    $envExamplePath = Join-Path $projectRoot ".env.example"
    if (-not (Test-Path $envPath)) {
        if (-not (Test-Path $envExamplePath)) {
            throw "Neither .env nor .env.example exists."
        }

        Copy-Item -LiteralPath $envExamplePath -Destination $envPath
        Write-Host "Created .env from .env.example."
    }

    if (-not (Test-Path (Join-Path $projectRoot ".venv"))) {
        Write-Host "Installing backend dependencies..."
        & uv sync --directory $projectRoot
        if ($LASTEXITCODE -ne 0) {
            throw "Backend dependency installation failed."
        }
    }

    if (-not (Test-Path (Join-Path $frontendRoot "node_modules"))) {
        Write-Host "Installing frontend dependencies..."
        & npm install --prefix $frontendRoot
        if ($LASTEXITCODE -ne 0) {
            throw "Frontend dependency installation failed."
        }
    }

    Write-Host "Starting backend at http://127.0.0.1:8000"
    Write-Host "Starting frontend at http://localhost:5173"
    Write-Host "Press Ctrl+C to stop both services."

    $jobs = @(
        Start-Job -Name "backend" -WorkingDirectory $projectRoot -ScriptBlock {
            [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
            $OutputEncoding = [System.Text.UTF8Encoding]::new()
            $env:PYTHONIOENCODING = "utf-8"
            $env:PYTHONUTF8 = "1"
            & uv run fastapi dev app/main.py 2>&1 |
                ForEach-Object { "[backend] $_" }
        }
        Start-Job -Name "frontend" -WorkingDirectory $frontendRoot -ScriptBlock {
            [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
            $OutputEncoding = [System.Text.UTF8Encoding]::new()
            & npm run dev 2>&1 |
                ForEach-Object { "[frontend] $_" }
        }
    )

    while ($true) {
        Receive-ServiceOutput -ServiceJobs $jobs

        $stoppedJob = $jobs |
            Where-Object { $_.State -in @("Completed", "Failed", "Stopped") } |
            Select-Object -First 1
        if ($null -ne $stoppedJob) {
            throw "The $($stoppedJob.Name) service exited with state $($stoppedJob.State)."
        }

        Start-Sleep -Milliseconds 200
    }
}
finally {
    if ($jobs.Count -gt 0) {
        Write-Host "Stopping services..."
        $jobs | Stop-Job -ErrorAction SilentlyContinue
        Receive-ServiceOutput -ServiceJobs $jobs
        $jobs | Remove-Job -Force -ErrorAction SilentlyContinue
    }
}
