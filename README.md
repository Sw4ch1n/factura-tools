# Factura Tools – Automatización de Procesamiento de Facturas

Aplicación desarrollada en Python con interfaz gráfica (Flet) para automatizar procesos relacionados con la gestión de facturas electrónicas (XML/PDF).

## 🚀 Funcionalidades principales

- 📦 Descompresión de archivos ZIP
- 📄 Validación de archivos XML y PDF
- 🧾 Renombrado automático usando UUID, fecha y emisor
- 🗂️ Organización en carpetas por fecha y razón social
- 📊 Generación automática de reportes en Excel
- 🖼️ Renombrado masivo de imágenes
- 🔄 Interfaz gráfica simple e intuitiva

## 🛠️ Tecnologías utilizadas

- Python 3
- Flet (interfaz gráfica)
- pandas, openpyxl (manejo de Excel)
- PyMuPDF (lectura de PDFs)
- unidecode, re, shutil, os, xml.etree

## 📁 Estructura del proyecto

```
factura-tools/
├── tools_1.4.0.py              # Interfaz principal
├── renamePdfUuid.py
├── renamePictures.py
├── extractZip.py
├── validationXmlPdf.py
├── processFiles.py
├── moveFilesRenamed.py
├── requirements.txt
└── README.md
```

## ▶️ Ejecución

1. Instala los requisitos:

```bash
pip install -r requirements.txt
```

2. Ejecuta la aplicación:

```bash
python tools_1.4.0.py
```

## 🧪 Requisitos

- Python 3.9+
- Windows 10 u 11 (por compatibilidad con Word, Excel y archivos del SAT)

## 🛡️ Notas

Este proyecto fue desarrollado como solución interna. No contiene información confidencial.

## 📄 Licencia

MIT
