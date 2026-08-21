@echo off
setlocal
cd /d "%~dp0\.."
title ProtegerDNI - Build Windows x64

echo ==========================================
echo     ProtegerDNI v1.5 - Windows x64
echo ==========================================
echo.

py -3.12-64 -c "import struct; assert struct.calcsize('P')*8 == 64; print('Python x64 OK')" || goto :python_error

py -3.12-64 -m pip install --upgrade pip
py -3.12-64 -m pip install -r requirements-build.txt
if errorlevel 1 goto :error

if exist build\x64 rmdir /s /q build\x64
if exist dist\x64 rmdir /s /q dist\x64
mkdir build\x64
mkdir dist\x64

py -3.12-64 -m PyInstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name "ProtegerDNI_x64" ^
  --icon "assets\ProtegerDNI.ico" ^
  --version-file "build\version_info.txt" ^
  --workpath "build\x64" ^
  --distpath "dist\x64" ^
  "src\ProtegerDNI.py"
if errorlevel 1 goto :error

echo.
echo SHA-256:
certutil -hashfile "dist\x64\ProtegerDNI_x64.exe" SHA256
echo.
echo Ejecutable:
echo %CD%\dist\x64\ProtegerDNI_x64.exe
explorer "%CD%\dist\x64"
pause
exit /b 0

:python_error
echo.
echo No se encontro Python 3.12 de 64 bits.
echo Instala Python 3.12 x64 y vuelve a ejecutar este BAT.
pause
exit /b 1

:error
echo.
echo ERROR DURANTE LA COMPILACION x64.
pause
exit /b 1
