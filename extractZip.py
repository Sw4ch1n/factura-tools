import flet as ft
import os
import zipfile

def process_zip_files(page: ft.Page, path: str):
    def mostrar_info(mensaje, titulo="Información"):
        dlg = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(dlg, "open", False), page.update()))]
        )
        page.open(dlg)
        page.update()

    try:
        archivos_zip = [f for f in os.listdir(path) if f.lower().endswith('.zip')]
        if archivos_zip:
            for zip_file in archivos_zip:
                ruta_zip = os.path.join(path, zip_file)
                try:
                    with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
                        zip_ref.extractall(path)
                        print(f"Extraído: {zip_file}")
                except zipfile.BadZipFile:
                    mostrar_info(f"El archivo {zip_file} no es un archivo ZIP válido.", "Error")
                except Exception as e:
                    mostrar_info(f"Error al extraer {zip_file}: {str(e)}", "Error")
            mostrar_info("Se encontraron y extrajeron archivos ZIP.", "Información")

    except FileNotFoundError:
        mostrar_info("La ruta especificada no existe.", "Error")
    except Exception as e:
        mostrar_info(f"Error inesperado: {str(e)}", "Error")