import os
import shutil
import xml.etree.ElementTree as ET
import fitz

def readXml(pathFile):
    try:
        ET.parse(pathFile)
        return False
    except ET.ParseError as e:
        print(f"Error de análisis XML {pathFile}: {e}")
        return True
    except FileNotFoundError:
        print(f"Archivo XML no encontrado: {pathFile}")
        return True
    except Exception as e:
        print(f"Error al leer XML {pathFile}: {e}")
        return True

def readPdf(pathFile):
    try:
        doc = fitz.open(pathFile)
        doc.load_page(0)
        return False
    except fitz.FileDataError as e:
        print(f"Error de datos PDF {pathFile}: {e}")
        return True
    except fitz.FileNotFoundError:
        print(f"Archivo PDF no encontrado: {pathFile}")
        return True
    except Exception as e:
        print(f"Error al leer PDF {pathFile}: {e}")
        return True
    finally:
        try:
            doc.close()
        except:
            pass

def moveFilesErrors(carpeta):
    if not os.path.exists(carpeta):
        print(f"La carpeta no existe: {carpeta}")
        return

    archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(('.xml', '.pdf'))]
    contador = 1
    errores_folder = None

    for archivo in archivos:
        pathFile = os.path.join(carpeta, archivo)
        if archivo.lower().endswith('.xml'):
            if readXml(pathFile):
                if errores_folder is None:
                    errores_folder = os.path.join(carpeta, '_archivos_con_errores')
                    os.makedirs(errores_folder, exist_ok=True)
                nuevo_nombre = f"error_{contador}.xml"
                nueva_ruta = os.path.join(errores_folder, nuevo_nombre)
                shutil.move(pathFile, nueva_ruta)
                print(f"Archivo XML {archivo} movido y renombrado a {nuevo_nombre}")
                contador += 1
        elif archivo.lower().endswith('.pdf'):
            if readPdf(pathFile):
                if errores_folder is None:
                    errores_folder = os.path.join(carpeta, 'errores')
                    os.makedirs(errores_folder, exist_ok=True)
                nuevo_nombre = f"error_{contador}.pdf"
                nueva_ruta = os.path.join(errores_folder, nuevo_nombre)
                shutil.move(pathFile, nueva_ruta)
                print(f"Archivo PDF {archivo} movido y renombrado a {nuevo_nombre}")
                contador += 1