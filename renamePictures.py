import flet as ft
import os
import time

def rename_pictures(page: ft.Page, selectPath: ft.FilePicker):
    def mostrar_alerta(mensaje):
        dlg = ft.AlertDialog(
            title=ft.Text("Atención"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(dlg, "open", False), page.update()))]
        )
        page.open(dlg)
        page.update()

    def mostrar_info(mensaje):
        dlg = ft.AlertDialog(
            title=ft.Text("Información"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(dlg, "open", False), page.update()))]
        )
        page.open(dlg)
        page.update()


    def process_directory(path):
        if not path:
            return

        if not os.path.isdir(path):
            mostrar_alerta("La ruta especificada no es válida. Inténtalo de nuevo.")
            return

        extensiones = ('.jpg', '.jpeg', '.bmp', '.png', '.gif', '.tiff')
        archivos = [f for f in os.listdir(path) if f.lower().endswith(extensiones)]
        archivos.sort()

        if not archivos:
            mostrar_alerta("No se encontraron imágenes en la carpeta seleccionada.")
            return

        renamed_files = []
        for archivo in archivos:
            try:
                extension = os.path.splitext(archivo)[1]
                timestamp = int(time.time() * 1000)
                nuevo_nombre = f"{timestamp}{extension}"
                ruta_original = os.path.join(path, archivo)
                ruta_nueva = os.path.join(path, nuevo_nombre)

                # Intentar renombrar varias veces con un retraso
                for _ in range(3):
                    try:
                        os.rename(ruta_original, ruta_nueva)
                        renamed_files.append((archivo, nuevo_nombre))
                        print(nuevo_nombre)
                        break  # Renombrado exitoso, salir del bucle
                    except OSError:
                        time.sleep(0.1)  # Esperar un poco antes de intentar de nuevo
                else:
                    mostrar_alerta(f"No se pudo renombrar {archivo} después de varios intentos.")
                    print("No se pudo renombrar {archivo}")

            except Exception as ex:
                mostrar_alerta(f"Error inesperado al renombrar {archivo}: {ex}")

        mostrar_info("Renombrado de imágenes completado.")

    selectPath.on_result = lambda e: process_directory(e.path)
    selectPath.get_directory_path()