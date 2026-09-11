$ErrorActionPreference = 'Stop'
$taskData = if ($env:OBS_DATA_DIR) { $env:OBS_DATA_DIR } else { Join-Path $PSScriptRoot 'data' }
$taskPidFile = Join-Path $taskData 'server-process.json'
if (-not (Test-Path -LiteralPath $taskPidFile)) { Write-Host 'Nenhum processo registrado. Se aberto numa janela, use Ctrl+C.'; exit 0 }
$taskInfo = Get-Content -LiteralPath $taskPidFile -Raw | ConvertFrom-Json
if ($taskInfo.root -ne $PSScriptRoot) { throw 'O processo registrado pertence a outra pasta. Encerramento cancelado.' }
$taskProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $([int]$taskInfo.pid)" -ErrorAction SilentlyContinue
if ($taskProcess) {
    if ($taskProcess.ExecutablePath -ne $taskInfo.executable -or $taskProcess.CommandLine -notmatch 'launcher\.py') { throw 'O processo mudou. Encerramento cancelado para preservar outros programas.' }
    Stop-Process -Id ([int]$taskInfo.pid)
}
Remove-Item -LiteralPath $taskPidFile -ErrorAction SilentlyContinue
Write-Host 'Observatorio encerrado. Seu acervo foi preservado.'
