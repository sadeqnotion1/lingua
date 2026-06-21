@echo off
setlocal
cd /d "%~dp0"
echo Starting Antigravity Skills Installer...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_skills.ps1"
pause
