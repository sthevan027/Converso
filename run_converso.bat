@echo off
REM Launcher do Converso: cria/verifica o ambiente virtual e inicia a GUI.
REM Use este script em vez de "python run_gui.py" para garantir venv e dependências.

set "ROOT=%~dp0"
set "VENV=%ROOT%.venv"
set "PY=%VENV%\Scripts\python.exe"
set "PIP=%VENV%\Scripts\pip.exe"
set "ACTIVATE=%VENV%\Scripts\activate.bat"

cd /d "%ROOT%"

if not exist "%PY%" (
    echo [Converso] Ambiente virtual nao encontrado. Criando .venv...
    python -m venv .venv
    if errorlevel 1 (
        echo Erro ao criar o ambiente virtual. Verifique se o Python esta instalado.
        pause
        exit /b 1
    )
    echo [Converso] Ambiente virtual criado.
)

if not exist "%PIP%" (
    echo [Converso] pip nao encontrado no venv. Recriando...
    "%PY%" -m ensurepip --upgrade
)

echo [Converso] Verificando dependencias...
"%PIP%" install -r requirements.txt -q
if errorlevel 1 (
    echo Aviso: algum pacote pode ter falhado. Tentando iniciar mesmo assim.
)

echo [Converso] Iniciando a aplicacao...
"%PY%" run_gui.py
exit /b %ERRORLEVEL%
