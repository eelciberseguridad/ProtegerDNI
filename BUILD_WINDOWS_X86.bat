@echo off
setlocal
cd /d "%~dp0\.."
title ProtegerDNI - Build Windows x86

echo ==========================================
echo     ProtegerDNI v1.5 - Windows x86
echo ==========================================
echo.

py -3.12-32 -c "import struct; assert struct.calcsize('P')*8 == 32; print('Python x86 OK')" || goto :python_error

py -3.12-32 -m pip install --upgrade pip
py -3.12-32 -m pip install -r requirements-build.txt
if errorlevel 1 goto :error

if exist build\x86 rmdir /s /q build\x86
if exist dist\x86 rmdir /s /q dist\x86
mkdir build\x86
mkdir dist\x86

py -3.12-32 -m PyInstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name "ProtegerDNI_x86" ^
  --icon "assets\ProtegerDNI.ico" ^
  --version-file "build\version_info.txt" ^
  --workpath "build\x86" ^
  --distpath "dist\x86" ^
  "src\ProtegerDNI.py"
if errorlevel 1 goto :error

echo.
echo SHA-256:
certutil -hashfile "dist\x86\ProtegerDNI_x86.exe" SHA256
echo.
echo Ejecutable:
echo %CD%\dist\x86\ProtegerDNI_x86.exe
explorer "%CD%\dist\x86"
pause
exit /b 0

:python_error
echo.
echo No se encontro Python 3.12 de 32 bits.
echo Instala Python 3.12 x86 y vuelve a ejecutar este BAT.
pause
exit /b 1

:error
echo.
echo ERROR DURANTE LA COMPILACION x86.
pause
exit /b 1
