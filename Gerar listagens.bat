@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo Python 3 nao encontrado. Instale o Python 3 e marque "Add Python to PATH".
  pause
  exit /b 1
)
python -c "import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)" >nul 2>nul
if errorlevel 1 (
  echo O comando python encontrado nao e Python 3. Instale o Python 3 e marque "Add Python to PATH".
  pause
  exit /b 1
)

set "ORIGEM=%~1"
if not defined ORIGEM (
  set /p "ORIGEM=Digite o caminho da pasta raiz da biblioteca virtual: "
)
if not defined ORIGEM (
  echo Nenhum caminho informado. Nada foi gravado.
  pause
  exit /b 1
)

set "EXTRA="
set "MANGAS=N"
set /p "MANGAS=Incluir tambem a subpasta de mangas dentro de HQs, se existir? (S/N): "
if /i "%MANGAS%"=="S" set "EXTRA=--incluir-conhecidas"

echo.
echo Previa das listagens que seriam geradas:
python tools\gerar_listagens.py --origem "%ORIGEM%" %EXTRA% --conferir
if errorlevel 1 (
  pause
  exit /b 1
)

echo.
set "CONFIRMA=N"
set /p "CONFIRMA=Gravar as listagens acima? (S/N): "
if /i not "%CONFIRMA%"=="S" (
  echo Nada foi gravado.
  pause
  exit /b 0
)

python tools\gerar_listagens.py --origem "%ORIGEM%" %EXTRA%
if errorlevel 1 (
  pause
  exit /b 1
)

echo.
echo Proximo passo: envie a pasta biblioteca-virtual\listagens para o GitHub
echo e peca: "atualize a biblioteca virtual".
pause
