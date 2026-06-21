@echo off
REM ====================================================================
REM  Launcher for LinguaRead - keeps the repo root clean.
REM  chcp 65001 makes Nerd Font glyphs + box characters render correctly.
REM  For the FULL look, launch from Windows Terminal with a Nerd Font.
REM ====================================================================
chcp 65001 >nul
setlocal
cd /d "%~dp0"

python "%~dp0backend\main.py" %*
set EXITCODE=%ERRORLEVEL%

if not "%EXITCODE%"=="0" (
  echo.
  echo  Launcher stopped with code %EXITCODE%.
  pause
)
endlocal
