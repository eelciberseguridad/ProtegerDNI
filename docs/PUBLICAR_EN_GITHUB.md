# PUBLICACIÓN EN GITHUB — ProtegerDNI v1.5

## 1. Nombre del repositorio

`ProtegerDNI`

## 2. Descripción corta del repositorio

> Herramienta gratuita para Windows que permite minimizar datos, individualizar y proteger copias de documentos de identidad antes de compartirlas.

## 3. Website

Puede dejarse vacío inicialmente.

## 4. Topics recomendados

```text
privacy
cybersecurity
data-protection
identity-protection
dni
windows
python
security-tools
privacy-tools
personal-data
```

## 5. Visibilidad

**Public**

La finalidad del proyecto es que cualquier persona pueda descargar la herramienta y que el código pueda ser revisado.

## 6. Qué subir al repositorio

Subir el contenido de este ZIP manteniendo la estructura de carpetas.

No subir DNI reales, documentos de prueba que contengan datos personales ni archivos temporales.

## 7. Ejecutables

Los ejecutables para usuarios finales deberían distribuirse principalmente mediante **GitHub Releases**.

Archivos recomendados para cada release:

```text
ProtegerDNI_x64.exe
ProtegerDNI_x64_SHA256.txt
ProtegerDNI_x86.exe
ProtegerDNI_x86_SHA256.txt
```

El repositorio también contiene `/releases` como ubicación opcional si se desea conservar una copia de los binarios dentro del repositorio.

## 8. Primera Release

Tag:

`v1.5`

Título:

`ProtegerDNI v1.5 — Primera versión pública`

Utilizar como descripción el archivo:

`RELEASE_v1.5.md`

## 9. Recomendación para usuarios

La versión principal recomendada debe ser **x64**, porque es la adecuada para la enorme mayoría de equipos actuales con Windows 10 y Windows 11.

Mantener x86 como descarga alternativa para sistemas Windows de 32 bits.

## 10. Integridad

Publicar siempre SHA-256 junto al ejecutable.

Esto permite que quien descarga el programa pueda comprobar que el archivo recibido coincide con el publicado por el proyecto.

## 11. Issues

Activarlos para:

- errores;
- incompatibilidades;
- propuestas de mejora.

Advertencia recomendada:

> Nunca adjuntes fotografías de tu DNI ni información personal real a un issue.

## 12. Código fuente

Mantener visible `/src/ProtegerDNI.py`.

Esto permite que terceros puedan revisar técnicamente el comportamiento de la aplicación.

## 13. Licencia

El proyecto utiliza la licencia incluida en `LICENSE`: uso gratuito no comercial, código disponible para estudio, auditoría y modificación, y prohibición de venta sin autorización.

Por contener una restricción comercial, el proyecto no debe anunciarse como software Open Source aprobado por OSI.
