import flet as ft
import os
import re
import shutil

def moveFilesRenamed(page: ft.Page, carpeta, progress_bar: ft.ProgressBar):
    def mostrar_alerta(mensaje, titulo="Información"):
        dlg = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(dlg, "open", False), page.update()))]
        )
        page.open(dlg)
        page.update()

    if carpeta is None:
        mostrar_alerta("No se seleccionó ninguna carpeta. Operación cancelada.")
        return

    try:
        archivos = os.listdir(carpeta)
        total_archivos = len(archivos)
        archivos_validos = 0

        for archivo in archivos:
            if archivo.lower().endswith(('.xml', '.pdf')):
                match = re.match(r"(\d{2})\.(\d{2})\.(\d{4})_([A-Z0-9]+)_([A-Z0-9]+)_FACTURA\.(xml|pdf)", archivo, re.I)
                if match:
                    archivos_validos += 1

        if archivos_validos == 0:
            mostrar_alerta("No se encontraron archivos con el formato de nombre correcto. Renombre los archivos primero.")
            return

        for i, archivo in enumerate(archivos):
            if archivo.lower().endswith(('.xml', '.pdf')):
                match = re.match(r"(\d{2})\.(\d{2})\.(\d{4})_([A-Z0-9]+)_([A-Z0-9]+)_FACTURA\.(xml|pdf)", archivo, re.I)
                if match:
                    try:
                        dia, mes, anio, emisor, uuid, extension = match.groups()
                    except ValueError as ve:
                        print(f"Error al desempaquetar valores del archivo {archivo}: {str(ve)}")
                        continue
                    ruta_final = os.path.join(carpeta, anio, name_month(mes), emisor)
                    if not os.path.exists(ruta_final):
                        os.makedirs(ruta_final)
                    archivo_origen = os.path.join(carpeta, archivo)
                    archivo_destino = os.path.join(ruta_final, archivo)
                    if os.path.exists(archivo_destino):
                        archivo_destino = os.path.join(ruta_final, f"_dup{archivo}")
                    try:
                        shutil.move(archivo_origen, archivo_destino)
                        print(f"Archivo movido: {archivo_origen} a {archivo_destino}")
                    except Exception as e:
                        print(f"No se pudo mover {archivo_origen} a {archivo_destino}: {str(e)}")
                else:
                    print(f"Archivo no coincide con el patrón: {archivo}")

            # Actualizar barra de progreso
            porcentaje_avance = (i + 1) / total_archivos
            progress_bar.value = porcentaje_avance
            page.update()  # Asegurar que page.update() se llama dentro del bucle

        mostrar_alerta(f"Archivos organizados exitosamente en la carpeta: {carpeta}")
    except Exception as e:
        mostrar_alerta(f"Error al mover archivos: {str(e)}", "Error")
        
    print(f"Procesando archivo: {archivo}")
    print(f"Ruta de destino: {ruta_final}")
    print(f"Archivo origen: {archivo_origen}")
    print(f"Archivo destino: {archivo_destino}")

def name_month(mes):
    meses = {
        "01": "01. Enero", "02": "02. Febrero", "03": "03. Marzo", "04": "04. Abril",
        "05": "05. Mayo", "06": "06. Junio", "07": "07. Julio", "08": "08. Agosto",
        "09": "09. Septiembre", "10": "10. Octubre", "11": "11. Noviembre", "12": "12. Diciembre"
    }
    return meses.get(mes, "Mes no encontrado")