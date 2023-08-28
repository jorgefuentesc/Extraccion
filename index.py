

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from urllib.parse import urlparse, parse_qs
import re
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook
import datetime
import os


ruta_carpeta_actual = os.path.dirname(os.path.abspath(__file__))
class Pelicula:
    def __init__(self, titulo, formatos, horarios):
        self.titulo = titulo
        self.formatos = formatos
        self.horarios = horarios

chrome_driver_path = 'C:\\Users\\Jorge Fuentes\\OneDrive - Cinepolis\\Escritorio\\Extraccion\\chromedriver.exe'
website = 'https://www.cinemark.cl/cine?tag=572&cine=cinemark_mallplaza'
urls_cinemark = [
    'https://www.cinemark.cl/cine?tag=2305&cine=cinemark_mallplaza_arica',
    'https://www.cinemark.cl/cine?tag=2302&cine=cinemark_mallplaza_mirador_bio_bio',
    'https://www.cinemark.cl/cine?tag=2306&cine=cinemark_arauco_coronel',
    'https://www.cinemark.cl/cine?tag=520&cine=cinemark_mallplaza_iquique',
    'https://www.cinemark.cl/cine?tag=2308&cine=cinemark_open_la_calera',
    'https://www.cinemark.cl/cine?tag=2309&cine=cinemark_mallplaza_la_serena',
    'https://www.cinemark.cl/cine?tag=2301&cine=cinemark_portal_osorno',
    'https://www.cinemark.cl/cine?tag=2304&cine=cinemark_open_ovalle',
    'https://www.cinemark.cl/cine?tag=2303&cine=cinemark_open_rancagua',
    'https://www.cinemark.cl/cine?tag=517&cine=cinemark_rancagua',
    'https://www.cinemark.cl/cine?tag=512&cine=cinemark_alto_las_condes',
    'https://www.cinemark.cl/cine?tag=572&cine=cinemark_mallplaza_norte',
    'https://www.cinemark.cl/cine?tag=513&cine=cinemark_mallplaza_oeste',
    'https://www.cinemark.cl/cine?tag=519&cine=cinemark_mallplaza_tobalaba',
    'https://www.cinemark.cl/cine?tag=511&cine=cinemark_mallplaza_vespucio',
    'https://www.cinemark.cl/cine?tag=2307&cine=cinemark_mid_mall_maipu',
    'https://www.cinemark.cl/cine?tag=2300&cine=cinemark_portal_nunoa',
    'https://www.cinemark.cl/cine?tag=548&cine=cinemark_mallplaza_trebol',
    'https://www.cinemark.cl/cine?tag=514&cine=cinemark_espacio_urbano',
    'https://www.cinemark.cl/cine?tag=570&cine=cinemark_mall_marina',
            ]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

service = Service(executable_path=chrome_driver_path)

workbook = Workbook()
sheet = workbook.active
max_horarios = 20
header = ['Nombre del Cine', 'Fechas', 'Nombre de la Película']
for i in range(1, max_horarios + 1):
    header.append(f'Horario {i}')
sheet.append(header)


for sitioweb in urls_cinemark:

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(sitioweb)

    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-cookies__accept-button')))

    # Encontrar el botón de aceptar cookies y hacer clic en él
    aceptar_cookies_button = driver.find_element(By.CLASS_NAME, 'modal-cookies__accept-button')
    aceptar_cookies_button.click()


    wait = WebDriverWait(driver, 20)
    ul_element = wait.until(EC.presence_of_element_located((By.ID, 'billboard_days')))
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    horariost = {}  # Diccionario para agrupar películas por día


    for num, li_element in enumerate(li_elements):
        print("Haciendo clic en:", li_element.text)
        diate = li_element.text
        
        # Hacer clic en el botón dentro del elemento <li>
        button = li_element.find_element(By.TAG_NAME, 'button')
        actions = ActionChains(driver)
        actions.click(button).perform()
        
        # Esperar a que se cargue la información después del clic
        time.sleep(5)  # Puedes ajustar este tiempo según necesites
        wait.until(EC.presence_of_element_located((By.ID, 'billboard_days')))
        
        # Crear un nuevo objeto BeautifulSoup basado en el contenido actualizado de la página
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        
        movie_show_container = soup2.find(class_='movies-container')
        if movie_show_container:
            movie_boxes = movie_show_container.find_all(class_='movie-box')
        
            for movie_box in movie_boxes:
                titulo_local_cine = soup2.find(class_='grid-center-content-vertical')
                nombre_cine = titulo_local_cine.get_text().strip()
                hora_peli = movie_box.find_all(class_='box-movie-format')
                
                titulo_peli_test_a = movie_box.find('a')
                href_value = titulo_peli_test_a['href']
                parsed_url = urlparse(href_value)
                query_params = parse_qs(parsed_url.query)
                nombre_pelicula = query_params.get('pelicula', [''])[0]

                horarios_form = []
                for contenedor_format_y_hora in hora_peli:
                    horarios_for = contenedor_format_y_hora.find_all(class_='movie-times')
                    for hr_horario_for in horarios_for:
                        btn_content_hora = hr_horario_for.find_all(class_='btn btn-buy')
                        for btn in btn_content_hora:
                            horario_numero = btn.get_text().strip()
                            horarios_form.append(horario_numero)
                            
                pelicula = Pelicula(nombre_pelicula, '', horarios_form)

                if diate not in horariost:
                    horariost[diate] = []
                horariost[diate].append(pelicula)
        else:
            print("No se encontró el contenedor con clase 'movies-container'")

    # Imprimir las películas por día
    for dia, peliculas_en_dia in horariost.items():
        for pelicula in peliculas_en_dia:
            fila_pelicula = [nombre_cine, dia, pelicula.titulo] + pelicula.horarios
            sheet.append(fila_pelicula)



    driver.quit()
ruta_archivo = os.path.join(ruta_carpeta_actual, "horarios_peliculas.xlsx")
workbook.save(ruta_archivo)