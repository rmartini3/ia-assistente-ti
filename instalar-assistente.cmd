@echo off
setlocal

rem --- Identifica a pasta onde o .cmd foi executado (origem) ---
set "SOURCE=%~dp0"
for %%I in ("%SOURCE:~0,-1%") do set "SOURCE=%%~fI"

rem --- Pergunta pasta de instalação (padrão recomendado: C:\Windows\Temp\AssistenteIATI) ---
set "DEFAULT_INSTALL=C:\Windows\Temp\AssistenteIATI"
set /p INSTALLDIR=Digite a pasta de instalacao [%DEFAULT_INSTALL%]:
if "%INSTALLDIR%"=="" set "INSTALLDIR=%DEFAULT_INSTALL%"
for %%I in ("%INSTALLDIR%") do set "INSTALLDIR=%%~fI"

echo Destino: "%INSTALLDIR%"
if not exist "%INSTALLDIR%" mkdir "%INSTALLDIR%" >nul

rem --- Copia o projeto inteiro para o destino escolhido ---
echo Copiando arquivos...
robocopy "%SOURCE%" "%INSTALLDIR%" /E /XO /R:1 /W:1 >nul

rem --- Define o alvo principal do atalho (exe se existir, senão .bat) ---
set "TARGET=%INSTALLDIR%\run_app.exe"
if not exist "%TARGET%" set "TARGET=%INSTALLDIR%\app.exe"
if not exist "%TARGET%" set "TARGET=%INSTALLDIR%\executar-assistente.bat"

rem --- Se não houver exe, tenta criar venv e instalar dependências (se Python disponível) ---
where python >nul 2>nul
if %errorlevel%==0 if not exist "%INSTALLDIR%\.venv" (
    echo Criando venv e instalando dependencias...
    pushd "%INSTALLDIR%"
    python -m venv .venv
    call .venv\Scripts\activate
    pip install --no-cache-dir -r requirements.txt
    popd
) 

rem --- Garante um launcher .bat funcional quando nenhum .exe existir ---
if not exist "%INSTALLDIR%\run_app.exe" if not exist "%INSTALLDIR%\app.exe" if not exist "%TARGET%" (
    > "%TARGET%" (
        echo @echo off
        echo setlocal
        echo cd /d "%INSTALLDIR%"
        echo if exist ".venv\\Scripts\\activate.bat" call ".venv\\Scripts\\activate.bat"
        echo streamlit run app.py
        echo endlocal
    )
)

rem --- Cria atalho na Área de Trabalho apontando para TARGET ---
set "DESKTOP=%USERPROFILE%\Desktop"
powershell -NoLogo -NoProfile -Command ^
  "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('%DESKTOP%\Assistente IA TI.lnk');" ^
  "$s.TargetPath='%TARGET%';" ^
  "$s.WorkingDirectory='%INSTALLDIR%';" ^
  "$s.IconLocation='%INSTALLDIR%\favicon.ico';" ^
  "$s.Save()"

echo.
set /p CLEAN=Apagar origem (zip/pasta atual) apos instalar? [s/N]:
if /I "%CLEAN%"=="S" (
    for %%Z in ("%USERPROFILE%\Downloads\ia-assistente-ti*.zip") do if exist "%%Z" del "%%Z"
    if /I not "%SOURCE%"=="%INSTALLDIR%" rmdir /S /Q "%SOURCE%"
) 

echo.
echo Concluido. Atalho criado em "%DESKTOP%\Assistente IA TI.lnk".
pause

