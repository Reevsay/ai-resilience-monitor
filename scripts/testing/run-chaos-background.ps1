# PowerShell script to run chaos test in truly detached background process
param(
    [int]$Duration = 24,
    [int]$ChaosDuration = 60,
    [int]$NormalDuration = 30
)

$scriptPath = "$PSScriptRoot\chaos-test.py"
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$logFile = "chaos-test-background.log"
$logFileFull = Join-Path $projectRoot $logFile

# Remove old log if exists
if (Test-Path $logFileFull) {
    Remove-Item $logFileFull
}

# Start Python process completely detached
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$logFileFull = Join-Path $projectRoot $logFile

$processInfo.FileName = "python"
$processInfo.Arguments = "`"$scriptPath`" --duration $Duration --chaos-duration $ChaosDuration --normal-duration $NormalDuration"
$processInfo.UseShellExecute = $false
$processInfo.RedirectStandardOutput = $true
$processInfo.RedirectStandardError = $true
$processInfo.WorkingDirectory = $projectRoot
$processInfo.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo

# Create async output handlers
$outputHandler = {
    param($sender, $e)
    if ($e.Data) {
        Add-Content -Path $logFileFull -Value $e.Data
    }
}

$process.add_OutputDataReceived($outputHandler)
$process.add_ErrorDataReceived($outputHandler)

# Start process
$process.Start() | Out-Null
$process.BeginOutputReadLine()
$process.BeginErrorReadLine()

$processId = $process.Id

Write-Host "================================================================================"
Write-Host "🔥 CHAOS TEST STARTED IN BACKGROUND"
Write-Host "================================================================================"
Write-Host "Process ID: $processId"
Write-Host "Duration: $Duration hours"
Write-Host "Chaos duration: $ChaosDuration seconds"
Write-Host "Normal period: $NormalDuration seconds"
Write-Host "Log file: $logFileFull"
Write-Host "================================================================================"
Write-Host ""
Write-Host "To monitor progress:"
Write-Host "  Get-Content `"$logFileFull`" -Wait"
Write-Host ""
Write-Host "To check if still running:"
Write-Host "  Get-Process -Id $processId -ErrorAction SilentlyContinue"
Write-Host ""
Write-Host "To stop the test:"
Write-Host "  Stop-Process -Id $processId"
Write-Host ""
Write-Host "================================================================================"

# Save PID for later reference
$pidFile = Join-Path $projectRoot "chaos-test.pid"
$processId | Out-File $pidFile
Write-Host "✅ Process ID saved to $pidFile"
