# ProtegerDNI

**Una copia de tu DNI no debería convertirse en una copia reutilizable para cualquier finalidad.**

ProtegerDNI es una herramienta gratuita para Windows creada para que cualquier persona
pueda preparar una copia de su documento de identidad antes de enviarla: recortar la
imagen, ocultar manualmente datos innecesarios e individualizar la copia mediante una
marca de agua con destinatario y fecha.

**Versión:** 1.5  
**Autor:** Eduardo Ernesto Lecce  
**EEL CIBERSEGURIDAD**  
**Contacto:** eelciberseguridad@gmail.com

## Descargar

El proyecto está preparado para distribuir dos ejecutables portables:

- **ProtegerDNI_x64.exe** — Windows 10 y Windows 11 de 64 bits.
- **ProtegerDNI_x86.exe** — Windows 10 y Windows 11 de 32 bits.

Los ejecutables no necesitan una instalación tradicional. Antes de publicarlos se
recomienda acompañarlos con su **SHA-256** para permitir la comprobación de integridad.

## ¿Qué hace?

ProtegerDNI procesa el documento localmente en la computadora. Permite:

- cargar frente y dorso por separado;
- visualizar inmediatamente cada imagen;
- recortar manualmente el área del documento;
- ocultar manualmente uno o varios datos;
- deshacer ocultamientos y restablecer la imagen;
- indicar **“Para ser presentado ante”**;
- agregar la fecha;
- mostrar una marca de agua diagonal y semitransparente;
- ver los cambios en vivo;
- generar JPG independientes de frente y dorso;
- generar un PDF con ambas caras;
- proteger opcionalmente el PDF mediante contraseña;
- generar hashes del archivo mediante la herramienta incluida.

## Privacidad por diseño

La aplicación:

- trabaja localmente;
- no necesita subir el DNI a un servidor;
- no utiliza OCR;
- no incorpora telemetría;
- no crea una base de datos de documentos;
- no mantiene un registro de destinatarios;
- no modifica el archivo original.

El objetivo no es hacer que una copia sea imposible de utilizar indebidamente, sino
**reducir la información expuesta y limitar la reutilización de la copia fuera del
contexto para el cual fue creada**.

## Filosofía del proyecto

ProtegerDNI nace con una finalidad simple: **que cualquier persona pueda proteger mejor
una copia de su identidad sin tener que comprar software ni entregar el documento a un
servicio online**.

El código puede estudiarse, auditarse y modificarse. El uso y la redistribución
no comercial son gratuitos. **La venta del programa está prohibida sin autorización
expresa del autor.**

### Importante sobre “Open Source”

Como la licencia prohíbe la venta, técnicamente no corresponde presentarla como una
licencia *Open Source* aprobada por la OSI, ya que las licencias Open Source no pueden
restringir la redistribución comercial. El proyecto se publica como **código fuente
disponible, auditable y modificable, con uso gratuito no comercial**.

Ver [LICENSE](LICENSE).

## Verificación de integridad

Cada release debería incluir:

```text
ProtegerDNI_x64.exe
ProtegerDNI_x64_SHA256.txt

ProtegerDNI_x86.exe
ProtegerDNI_x86_SHA256.txt
```

El repositorio incluye `tools/CREAR_HASH.bat` para calcular hashes. Para verificar
integridad se recomienda **SHA-256**.

## Compilación

Los scripts incluidos permiten generar los ejecutables desde Windows:

```text
build/BUILD_WINDOWS_X64.bat
build/BUILD_WINDOWS_X86.bat
build/BUILD_BOTH.bat
```

También se incluye `.github/workflows/build-windows.yml`, que permite compilar ambas
arquitecturas mediante GitHub Actions.

## Documentación

- [Por qué proteger los datos](docs/POR_QUE_PROTEGER_DATOS.md)
- [Descripción técnica](docs/DESCRIPCION_TECNICA.md)
- [Compilación para Windows](docs/BUILD_WINDOWS.md)
- [Política de seguridad](SECURITY.md)

## Alcance

ProtegerDNI no verifica la autenticidad de un DNI, no sustituye sistemas oficiales de
identidad digital y no garantiza que una copia no pueda ser manipulada o reutilizada.
Es una herramienta de minimización, individualización y protección práctica de copias.

---

**ProtegerDNI — Creado por Eduardo Ernesto Lecce · EEL CIBERSEGURIDAD**
