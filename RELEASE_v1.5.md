# ProtegerDNI v1.5 — Primera versión pública

ProtegerDNI nace con una finalidad concreta: **permitir que cualquier persona pueda proteger mejor una copia de su documento de identidad antes de compartirla**.

Enviar una fotografía limpia del DNI genera una copia potencialmente reutilizable. Esta herramienta permite crear una copia específica para un destinatario y una fecha determinados, reduciendo además los datos visibles cuando no sean necesarios.

## Funciones de esta versión

- Carga independiente de frente y dorso.
- Vista previa inmediata.
- Recorte manual del documento.
- Ocultamiento manual de datos.
- Deshacer ocultamientos.
- Restablecimiento de la imagen.
- Individualización mediante **“Para ser presentado ante”**.
- Fecha.
- Marca de agua diagonal y semitransparente.
- Actualización de la marca en vivo.
- Exportación JPG.
- Exportación PDF.
- Protección opcional del PDF mediante contraseña.
- Procesamiento local.
- Sin OCR.
- Sin telemetría.
- Sin base de datos.
- Sin almacenamiento de destinatarios.

## Descargas

### Windows 64 bits — recomendada

`ProtegerDNI_x64.exe`

Para la mayoría de computadoras con Windows 10 y Windows 11.

### Windows 32 bits

`ProtegerDNI_x86.exe`

Para sistemas Windows de 32 bits.

## Comprobar integridad

Cada ejecutable se publica acompañado por un archivo TXT que contiene su **SHA-256**.

Antes de utilizarlo, el hash puede comprobarse en Windows con:

```powershell
Get-FileHash .\ProtegerDNI_x64.exe -Algorithm SHA256
```

El resultado debe coincidir exactamente con el SHA-256 publicado en esta release.

## Importante

ProtegerDNI no verifica la autenticidad de un documento y no garantiza que una copia no pueda ser manipulada o reutilizada. Es una herramienta para **minimizar exposición, individualizar una copia y reducir su reutilización fuera del contexto previsto**.

El usuario decide qué información debe permanecer visible según el trámite que vaya a realizar.

## Privacidad

El procesamiento se realiza localmente en la computadora. ProtegerDNI no necesita subir el documento a servidores, no incorpora OCR ni telemetría y no crea una base de datos de documentos.

## Licencia

Uso gratuito y no comercial. El código puede estudiarse, auditarse y modificarse bajo las condiciones de `LICENSE`.

**Está prohibida la venta del programa sin autorización expresa.**

---

**ProtegerDNI v1.5**  
Creado por **Eduardo Ernesto Lecce**  
**EEL CIBERSEGURIDAD**  
eelciberseguridad@gmail.com
