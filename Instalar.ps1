$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$taskPython = $null
$taskArguments = @()
if (Get-Command py -ErrorAction SilentlyContinue) {
    $taskPython = (Get-Command py).Source
    $taskArguments = @('-3')
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $taskPython = (Get-Command python).Source
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $taskPython = (Get-Command python3).Source
} else {
    Write-Host 'Instale Python 3.11 ou superior de https://www.python.org/downloads/ e marque Add Python to PATH.'
    exit 1
}
& $taskPython @taskArguments -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'
if ($LASTEXITCODE -ne 0) { throw 'E necessario Python 3.11 ou superior.' }
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    & $taskPython @taskArguments -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao criar o ambiente Python local.' }
}
& '.\.venv\Scripts\python.exe' -m pip install -r requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar dependencias. Confira sua conexao e tente novamente.' }
Write-Host 'Instalacao concluida. Abra Iniciar.cmd. Seu acervo existente foi preservado.'
