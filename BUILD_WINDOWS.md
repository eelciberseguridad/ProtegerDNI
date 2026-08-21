# Compilación para Windows 10 y Windows 11

## Arquitecturas

Se proporcionan dos compilaciones independientes:

- `ProtegerDNI_x64.exe`: Windows 10/11 de 64 bits.
- `ProtegerDNI_x86.exe`: Windows 10/11 de 32 bits y, normalmente, Windows x64 con soporte WoW64.

Un ejecutable creado con Python de 64 bits no debe tratarse como un binario universal de 32/64 bits. Para obtener x86 se compila con Python x86; para obtener x64 se compila con Python x64.

## Requisitos para compilar localmente

Instalar Python 3.12 en la arquitectura correspondiente.

### x64

Ejecutar:

```bat
build\BUILD_WINDOWS_X64.bat
```

### x86

Ejecutar:

```bat
build\BUILD_WINDOWS_X86.bat
```

### Ambas

```bat
build\BUILD_BOTH.bat
```

## GitHub Actions

El workflow `.github/workflows/build-windows.yml` crea automáticamente artefactos x64 y x86 en un runner Windows usando una matriz de arquitecturas.

Puede ejecutarse manualmente desde **Actions → Build Windows Portables → Run workflow** o automáticamente al crear una etiqueta `v*`.

## Validación recomendada

Antes de publicar una release, probar ambos ejecutables al menos en:

- Windows 10 x64;
- Windows 11 x64;
- Windows 10 x86, si se dispone de ese entorno;
- una cuenta estándar sin Python instalado.

También conviene verificar:

- apertura de frente y dorso;
- recorte;
- ocultamiento y deshacer;
- marca de agua en vivo;
- generación JPG;
- generación PDF;
- PDF con contraseña;
- SHA-256 del ejecutable.
