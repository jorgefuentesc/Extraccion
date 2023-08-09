# from bs4 import BeautifulSoup
# from selenium import webdriver
# from urllib.parse import urlparse, parse_qs
# from selenium.webdriver.chrome.service import Service
# import time
# import re

# chrome_driver_path = 'C:\\Users\\Jorge Fuentes\\OneDrive - Cinepolis\\Escritorio\\Extraccion\\chromedriver.exe'
# website = 'https://www.cinemark.cl/cine?tag=572&cine=cinemark_mallplaza'

# chrome_options = webdriver.ChromeOptions()
# service = Service(executable_path=chrome_driver_path)
# driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.get(website)

# time.sleep(5)
# content = driver.page_source
# driver.quit()

# cine_name = ""
# peliculas = []

# soup = BeautifulSoup(content, 'html.parser')
# movie_show_container = soup.find(class_='movies-container')

# if movie_show_container:
#     movie_boxes = movie_show_container.find_all(class_='movie-box')
    
#     for movie_box in movie_boxes:
#         horas_esp = movie_box.find_all(class_='movie-schedule')
#         hora_peli = movie_box.find_all(class_ = 'box-movie-format')
#         titulo_peli = movie_box.find(class_ = 'movie-title')
#         titulo_peli_test_a = movie_box.find('a')
#         href_value = titulo_peli_test_a['href']
#         parsed_url = urlparse(href_value)
#         query_params = parse_qs(parsed_url.query)
#         nombre_pelicula = query_params.get('pelicula', [''])[0]


#         horarios = [hora.get_text() for hora in hora_peli]
#         funciones = [funcion.get_text() for funcion in horas_esp]
#         pattern = r'\b\d{1,2}:\d{2}\b'

#         horas_coincidencias = re.findall(pattern, funciones)
#         horas_funciones = [hora for hora in horas_coincidencias]

#         # print("test guardado_horario", horarios)
#         print("test guardado_funciones", horas_funciones)

#         print(nombre_pelicula)
#         for peli_hora in hora_peli:
#             hour = peli_hora.get_text()
#         #     print("--",hour)
        
#         # print("-" * 30)
# else:
#     print("No se encontró el contenedor con clase 'movies-container'")


from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.chrome.service import Service
import time
import re
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

chrome_driver_path = 'C:\\Users\\Jorge Fuentes\\OneDrive - Cinepolis\\Escritorio\\Extraccion\\chromedriver.exe'
website = 'https://www.cinemark.cl/cine?tag=572&cine=cinemark_mallplaza'

chrome_options = webdriver.ChromeOptions()
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)

time.sleep(5)
content = driver.page_source
driver.quit()

cine_name = ""
peliculas = []

soup = BeautifulSoup(content, 'html.parser')
movie_show_container = soup.find(class_='movies-container')

if movie_show_container:
    document = Document()
    movie_boxes = movie_show_container.find_all(class_='movie-box')
    
    for movie_box in movie_boxes:
        horas_esp = movie_box.find_all(class_='movie-schedule')
        hora_peli = movie_box.find_all(class_='box-movie-format')
        titulo_peli = movie_box.find(class_='movie-title')
        titulo_peli_test_a = movie_box.find('a')
        href_value = titulo_peli_test_a['href']
        parsed_url = urlparse(href_value)
        query_params = parse_qs(parsed_url.query)
        nombre_pelicula = query_params.get('pelicula', [''])[0]

        horarios = [hora.get_text() for hora in hora_peli]

        # Obtener el texto completo de las funciones
        funciones_texto = [funcion.get_text() for funcion in horas_esp]

        # Procesar el texto de las funciones y extraer descripciones y horas
        horas_funciones = {}
        descripcion = ""
        for funcion_texto in funciones_texto:
            if re.match(r'^\d{1,2}:\d{2}', funcion_texto):
                horas = re.findall(r'\d{1,2}:\d{2}', funcion_texto)
                horas_funciones[descripcion] = horas
            else:
                descripcion = funcion_texto.strip()
        

        document.add_heading(nombre_pelicula, level=1)
        document.add_paragraph("Descripción: " + descripcion)
        document.add_paragraph("Horarios: " + ', '.join(horarios))
        for desc, horas in horas_funciones.items():
            document.add_paragraph(f"{desc}: {', '.join(horas)}")
        document.add_page_break()
    
        print("Archivo Word 'peliculas_cinemark.docx' creado exitosamente.")
        print("Nombre de la película:", nombre_pelicula)
        print("Descripción:", descripcion)
        print("Horas de funciones:", horas_funciones)
        print("-" * 30)
else:
    print("No se encontró el contenedor con clase 'movies-container'")
