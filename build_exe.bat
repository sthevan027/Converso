@echo off
REM Gera o executável Converso.exe (não precisa rodar "python run_gui.py" depois).
REM Requer: pip install -r requirements.txt (inclui pyinstaller)

echo Instalando PyInstaller se necessário...
pip install pyinstaller>=6.0.0 --quiet

echo.
echo Gerando o executável...
pyinstaller converso.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Pronto. O executável está em: dist\Converso.exe
    echo Você pode copiar dist\Converso.exe para qualquer pasta e executar com duplo clique.
) else (
    echo.
    echo Erro na geração. Verifique as mensagens acima.
    exit /b 1
)
