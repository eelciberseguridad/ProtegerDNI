# Descripción técnica de ProtegerDNI v1.5

ProtegerDNI es una aplicación de escritorio portable orientada a generar copias individualizadas de documentos de identidad.

## Procesamiento

- La aplicación trabaja localmente sobre imágenes cargadas por el usuario.
- No requiere conexión a Internet.
- No utiliza OCR.
- No identifica automáticamente campos del documento.
- No crea una base de datos.
- No mantiene historial permanente de documentos procesados.
- No modifica los archivos originales.

## Frente y dorso

Cada cara se procesa de forma independiente.

Al cargar una imagen, la aplicación presenta una vista previa inmediata. El usuario puede:

- recortar manualmente la fotografía para conservar únicamente el documento;
- mover y ajustar el área de recorte antes de aceptarla;
- ocultar manualmente una o varias áreas;
- deshacer el último ocultamiento;
- restablecer la imagen de trabajo;
- cancelar una edición;
- aceptar el resultado y volver a la vista principal.

## Individualización

La copia permite indicar:

- destinatario mediante el campo **Para ser presentado ante**;
- fecha.

Ambos datos se representan mediante una marca de agua diagonal, central y semitransparente. La vista previa se actualiza mientras se modifican estos campos.

## Exportación JPG

Genera dos imágenes independientes:

- `DNIProtegido_Frente.jpg`
- `DNIProtegido_Dorso.jpg`

El usuario elige nombre y ubicación mediante el cuadro Guardar como.

## Exportación PDF

Genera un PDF con frente y dorso. De forma opcional puede cifrarse con contraseña.

La exportación PDF utiliza un archivo temporal durante la generación y posteriormente intenta eliminarlo.

## Metadatos

Las imágenes cargadas se convierten a RGB y se vuelven a generar durante el procesamiento, evitando trasladar directamente los metadatos EXIF originales a la salida JPG generada por la aplicación.

## Marca de agua

La marca de agua:

- contiene destinatario y fecha;
- se coloca en diagonal en la zona central;
- utiliza transparencia;
- no incorpora QR ni identificadores persistentes.

## Herramienta de hash

El proyecto incluye `CREAR_HASH.bat`, que calcula:

- SHA-256;
- SHA-1;
- MD5.

El reporte se escribe en un TXT junto al archivo analizado. Para comprobación de integridad se recomienda SHA-256.

## Alcance

ProtegerDNI no verifica la autenticidad de un documento, no sustituye mecanismos oficiales de identidad digital y no impide por sí mismo la extracción de datos visibles. Su finalidad es generar una copia de propósito limitado y reducir la exposición y reutilización innecesaria.
