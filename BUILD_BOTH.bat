@echo off
setlocal
cd /d "%~dp0"
call BUILD_WINDOWS_X64.bat
if errorlevel 1 echo La compilacion x64 no se completo.
call BUILD_WINDOWS_X86.bat
if errorlevel 1 echo La compilacion x86 no se completo.
echo.
echo Proceso finalizado.
pause
