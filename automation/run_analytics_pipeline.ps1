param(
    [switch]$IncludeYellow
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogDir = Join-Path $ScriptDir "logs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$Timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
$LogFile = Join-Path $LogDir "analytics-pipeline-$Timestamp.log"

function Write-Log {
    param([string]$Message)
    $line = "$(Get-Date -Format s) $Message"
    $line | Tee-Object -FilePath $LogFile -Append
}

try {
    Write-Log "Starting In Project analytics automation."

    $Python = Get-Command py -ErrorAction SilentlyContinue
    if ($null -eq $Python) {
        $Python = Get-Command python -ErrorAction SilentlyContinue
    }
    if ($null -eq $Python) {
        throw "Python was not found. Install Python or add it to PATH."
    }

    $Args = @(
        (Join-Path $ScriptDir "generate_management_alerts.py"),
        "--input", "../analysis/tables/project_performance_analysis.csv",
        "--output", "output/management_alerts.csv"
    )
    if ($IncludeYellow) {
        $Args += "--include-yellow"
    }

    & $Python.Source @Args 2>&1 | Tee-Object -FilePath $LogFile -Append
    if ($LASTEXITCODE -ne 0) {
        throw "The alert-generation script failed with exit code $LASTEXITCODE."
    }

    Write-Log "Automation completed successfully."
    Write-Log "Next cloud step: trigger the Power BI semantic-model refresh or allow the scheduled refresh to run."
}
catch {
    Write-Log "FAILED: $($_.Exception.Message)"
    exit 1
}
