@echo off
setlocal
rem Wrapper: runs pack.ps1 (ASCII-only on purpose, so console code page does not matter).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pack.ps1"
if errorlevel 1 (
  echo.
  echo Packaging failed. See the messages above.
  pause
)
