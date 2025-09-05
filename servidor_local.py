from flask import Flask, request, jsonify
import re
import os
from pathlib import Path
from playwright.sync_api import Playwright, sync_playwright, expect
from time import sleep
from os import remove
from datetime import datetime

def Registro_Lote_Campus_Virtual(playwright: Playwright,archivo,nombre_aplicativo) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://pandora.pucp.edu.pe/pucp/login?TARGET=https%3A%2F%2Feros.pucp.edu.pe%2Fpucp%2Fjsp%2FIntranet.jsp")
    page.locator("#username").fill("W0026391")
    page.locator("#username").press("Tab")
    page.locator("#password").fill("TyS_idiomas.25.2")
    page.locator("#password").press("Tab")
    page.get_by_role("link").filter(has_text=re.compile(r"^$")).press("Enter")
    page.locator("#menu-toggle div").nth(1).click()
    page.get_by_text("Universidad").click()
    page.get_by_text("Organización").click()
    page.locator("iframe[name=\"frame_mid\"]").content_frame.get_by_role("link", name="Idiomas Católica").click()
    page.locator("iframe[name=\"frame_mid\"]").content_frame.get_by_role("button", name="Alumno").click()
    page.locator("iframe[name=\"frame_mid\"]").content_frame.get_by_role("link", name=nombre_aplicativo).click()
    dir_actual = Path.cwd()
    file_input = page.locator('iframe[name="frame_mid"]').content_frame.locator('input[type="file"]')
    file_input.wait_for(state="visible", timeout=5000)
    file_input.set_input_files(str(archivo))
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator("iframe[name=\"frame_mid\"]").content_frame.get_by_role("button", name="Procesar").click()
    with page.expect_download() as download_info:
        page.locator("iframe[name=\"frame_mid\"]").content_frame.get_by_role("link", name="aquí").click()
    download = download_info.value
    Archivo_a_Crear2 = "DetalleLote.xls"
    dir_actual = Path.cwd()
    dir_con_archivo2 = dir_actual / Archivo_a_Crear2
    #download.save_as(dir_con_archivo2)
    page.locator("iframe[name=\"frame_mid\"]").content_frame.get_by_role("button", name="Regresar").click()

        
    # ---------------------
    context.close()
    browser.close()


app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def recibir_datos():
    datos = request.json
    print("Datos recibidos:", datos)
    # Aquí puedes guardar los datos o procesarlos


    with sync_playwright() as playwright:
        Registro_Lote_Campus_Virtual(playwright,"datos.csv","Creación masiva de alumnos")
    remove(str(dir_con_archivo))

    return jsonify({"status": "ok papu"}), 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)

