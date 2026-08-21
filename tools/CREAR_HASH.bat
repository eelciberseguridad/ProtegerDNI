@echo off
setlocal
title Creador de Hash - EEL CIBERSEGURIDAD
echo ==========================================
echo    CREADOR DE HASH - EEL CIBERSEGURIDAD
echo ==========================================
echo.
set "archivo=%~1"
if not defined archivo (
    set /p "archivo=Arrastra el archivo a esta ventana o escribe su ruta completa: "
)
set "archivo=%archivo:"=%"
if not exist "%archivo%" (
    echo.
    echo ERROR: El archivo no existe.
    pause
    exit /b 1
)
echo.
echo Archivo: %archivo%
echo.
echo SHA-256:
certutil -hashfile "%archivo%" SHA256
echo.
echo SHA-1:
certutil -hashfile "%archivo%" SHA1
echo.
echo MD5:
certutil -hashfile "%archivo%" MD5
echo.
echo Nota: SHA-256 es el hash recomendado para integridad.
echo.
pause
