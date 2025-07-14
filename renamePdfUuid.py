import fitz
import os
import re
import time
import logging

logging.basicConfig(level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

def extractUuidPdf(pdf_path):
    folio_fiscal_pattern = re.compile(r'Folio Fiscal:\s*([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})')
    uuid_pattern = re.compile(r'\b[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}\b')

    try:
        document = fitz.open(pdf_path)
        full_text = "\n".join([page.get_text() for page in document])

        folio_match = folio_fiscal_pattern.search(full_text)
        if folio_match:
            return folio_match.group(1).upper().replace('-', '')

        match = uuid_pattern.search(full_text)
        if match:
            return match.group(0).upper().replace('-', '')

    except (OSError, fitz.FileNotFoundError, fitz.UnknownFiletypeError, fitz.InvalidFileError) as e:
        logging.error(f"Error al abrir el PDF {pdf_path}: {e}")
    except Exception as e:
        logging.error(f"Error inesperado al procesar {pdf_path}: {e}")
    finally:
        try:
            document.close()
        except:
            pass

    return None

def generateUniqueFilename(dir_path, base_name):
    base_path = os.path.join(dir_path, base_name + ".pdf")
    if not os.path.exists(base_path):
        return base_path

    suffix = 1
    while True:
        new_path = os.path.join(dir_path, f"FD{suffix}_{base_name}.pdf")
        if not os.path.exists(new_path):
            return new_path
        suffix += 1

def renamePdfWithUuid(pdf_path, uuid):
    dir_path, original_filename = os.path.split(pdf_path)
    new_path = generateUniqueFilename(dir_path, uuid)

    time.sleep(0.1)

    try:
        os.rename(pdf_path, new_path)
        logging.info(f"Renamed {original_filename} to {os.path.basename(new_path)}")
    except OSError as e:
        logging.error(f"No se pudo renombrar {pdf_path}: {e}")

def processPdfs(directory):
    if not os.path.exists(directory):
        logging.error(f"El directorio no existe: {directory}")
        return
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            uuid = extractUuidPdf(pdf_path)
            if uuid and re.match(r'^[0-9A-F]{32}$', uuid): #Validación del UUID
                renamePdfWithUuid(pdf_path, uuid)
            else:
                logging.warning(f"UUID no válido o no encontrado en {filename}")