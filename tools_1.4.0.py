import flet as ft
import getpass
import time
import renamePictures
import extractZip
import validationXmlPdf
import renamePdfUuid
import processFiles
import moveFilesRenamed
import os
import subprocess

usuario = getpass.getuser()

def main(page: ft.Page):
    page.title = "Herramienta para renombrar facturas e Imagenes"
    page.window.resizable = False
    page.window.width = 800
    page.window.height = 600
    progress_bar = ft.ProgressBar(width=600, height=15, value=0, visible=False)
    lbl_progreso = ft.Text(value="", text_align=ft.TextAlign.CENTER, visible=False)
    col_progreso = ft.Column(controls=[progress_bar, lbl_progreso], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    lbl_bienvenida = ft.Text(
        value=f"\nHola {usuario} \n\nEsta herramienta ayuda a renombrar facturas de forma rápida.\n\nSelecciona una opción.",
        text_align=ft.TextAlign.CENTER,
        size=20,
    )

    selectedSucursal = ft.Ref[ft.Dropdown]()
    dropdown_sucursales = ft.Dropdown(
        ref=selectedSucursal,
        label="Sucursal",
        options=[
            ft.dropdown.Option("QUERETARO"),
            ft.dropdown.Option("CORDOBA"),
            ft.dropdown.Option("MERIDA"),
        ],
        width=200,
    )

    selectPathImg = ft.FilePicker()
    page.overlay.append(selectPathImg)

    selectPathFacturas = ft.FilePicker(on_result=lambda e: process_files(e.path, "Renombrando..."))
    page.overlay.append(selectPathFacturas)

    selectPathReorder = ft.FilePicker(on_result=lambda e: organize_facturas(e.path))
    page.overlay.append(selectPathReorder)

    def mostrar_alerta(mensaje):
        dlg = ft.AlertDialog(
            title=ft.Text("Atención"),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("OK", on_click=lambda e: (setattr(dlg, "open", False), page.update()))]
        )
        page.open(dlg)
        page.update()

    def runRenamePicture(e):
        renamePictures.rename_pictures(page, selectPathImg)
        if selectPathImg is None:
            mostrar_alerta("Selecciona una carpeta antes de continuar.")
            return

    def rename_facturas(e):
        if selectedSucursal.current.value is None:
            mostrar_alerta("Selecciona una sucursal antes de continuar.")
            return
        selectPathFacturas.get_directory_path()

    def process_files(carpeta, mensaje_progreso):
        if carpeta is None:
            mostrar_alerta("Selecciona una carpeta antes de continuar.")
            return
        try:
            progress_bar.visible = True
            progress_bar.value = 0
            lbl_progreso.value = mensaje_progreso
            lbl_progreso.visible = True
            page.update()

            extractZip.process_zip_files(page, carpeta)
            validationXmlPdf.moveFilesErrors(carpeta)
            renamePdfUuid.processPdfs(carpeta)
            processFiles.processFiles(page, carpeta, selectedSucursal.current.value, progress_bar)
            lbl_progreso.value = "Terminado"
            page.update()
            time.sleep(1)
            progress_bar.visible = False
            lbl_progreso.visible = False
            page.update()
        except Exception as e:
            mostrar_alerta(f"Error en el proceso: {str(e)}")
            progress_bar.visible = False
            lbl_progreso.visible = False
            page.update()

    def organize_facturas(ruta_origen): # Recibe ruta_origen directamente
        if ruta_origen is None:
            mostrar_alerta("Selecciona la carpeta de origen antes de continuar.")
            return
        try:
            progress_bar.visible = True
            progress_bar.value = 0
            lbl_progreso.value = "Organizando..."
            lbl_progreso.visible = True
            page.update()

            moveFilesRenamed.moveFilesRenamed(page, ruta_origen, progress_bar)
            lbl_progreso.value = "Terminado"
            page.update()
            time.sleep(1)
            progress_bar.visible = False
            lbl_progreso.visible = False
            page.update()
        except Exception as e:
            mostrar_alerta(f"Error en el proceso: {str(e)}")
            progress_bar.visible = False
            lbl_progreso.visible = False
            page.update()

    btn_img = ft.ElevatedButton(
        text="Renombrar Imágenes",
        on_click=runRenamePicture,
        width=200,
        height=50,
        style=ft.ButtonStyle(
        color=ft.colors.with_opacity(0.8, ft.colors.TEAL_400),
        text_style=ft.TextStyle(size=17, font_family="Roboto", weight=ft.FontWeight.BOLD),
        ),
    )
    
    btn_facturas = ft.ElevatedButton(
        text="Renombrar Facturas",
        on_click=rename_facturas,
        width=200,
        height=50,
        style=ft.ButtonStyle(
        color=ft.colors.with_opacity(0.8, ft.colors.TEAL_400),
        text_style=ft.TextStyle(size=17, font_family="Roboto", weight=ft.FontWeight.BOLD),
        ),
    )
    
    btn_organizar = ft.ElevatedButton(
        text="Organizar Facturas",
        on_click=lambda _: selectPathReorder.get_directory_path(),
        width=200,
        height=50,
        style=ft.ButtonStyle(
        color=ft.colors.with_opacity(0.8, ft.colors.TEAL_400),
        text_style=ft.TextStyle(size=17, font_family="Roboto", weight=ft.FontWeight.BOLD),
        ),
    )


    page.add(
        ft.Column(
            controls=[
                lbl_bienvenida,
                dropdown_sucursales,
                ft.Row(controls=[btn_img], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row(controls=[btn_facturas, btn_organizar], alignment=ft.MainAxisAlignment.CENTER),
                col_progreso
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    page.update()

ft.app(target=main)