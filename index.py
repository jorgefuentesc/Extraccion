# from bs4 import BeautifulSoup
# from selenium import webdriver
# from urllib.parse import urlparse, parse_qs
# from selenium.webdriver.chrome.service import Service
# import time
# import re
# from docx import Document
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

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
#         imagen_url = movie_box.find('a')
#         img_format = imagen_url['style']
#         start_index = img_format.find('"') + 1
#         end_index = img_format.find('"', start_index)
#         img_url = img_format[start_index:end_index]

#         print(img_url,"test img")
#         horas_esp = movie_box.find_all(class_='movie-schedule')
#         hora_peli = movie_box.find_all(class_='box-movie-format')
#         titulo_peli = movie_box.find(class_='movie-title')
#         titulo_peli_test_a = movie_box.find('a')
#         href_value = titulo_peli_test_a['href']
#         parsed_url = urlparse(href_value)
#         query_params = parse_qs(parsed_url.query)
#         nombre_pelicula = query_params.get('pelicula', [''])[0]

#         horarios = [hora.get_text() for hora in hora_peli]

#         # Obtener el texto completo de las funciones
#         funciones_texto = [funcion.get_text() for funcion in horas_esp]

#         # Procesar el texto de las funciones y extraer descripciones y horas
#         horas_funciones = {}
#         descripcion = ""
#         for funcion_texto in funciones_texto:
#             if re.match(r'^\d{1,2}:\d{2}', funcion_texto):
#                 horas = re.findall(r'\d{1,2}:\d{2}', funcion_texto)
#                 horas_funciones[descripcion] = horas
#             else:
#                 descripcion = funcion_texto.strip()
    
#         # print("Archivo Word 'peliculas_cinemark.docx' creado exitosamente.")
#         # print("Nombre de la película:", nombre_pelicula)
#         # print("Descripción:", descripcion)
#         # print("Horas de funciones:", horas_funciones)
#         # print("-" * 30)
# else:
#     print("No se encontró el contenedor con clase 'movies-container'")





from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.chrome.service import Service
import time
import re
from reportlab.lib.pagesizes import letter
from docx import Document
from reportlab.pdfgen import canvas
import datetime
from selenium.webdriver.common.by import By




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
titulo_local_cine = soup.find(class_= 'grid-center-content-vertical')
titulo_formateado_cine = titulo_local_cine.get_text()

print(titulo_formateado_cine)
lista_botones = driver.find_elements(By.ID, 'billboard_days')
print(lista_botones," eee")


# pelis_dias = soup.find(class_='billboard-days')
# print(pelis_dias,"normal")
# print(pelis_dias.get_text(),"xxx")
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
        formato = ''
        
        for contenedor_format_y_hora in hora_peli:
            formatos_for = contenedor_format_y_hora.find(class_= 'movie-format' )
            horarios_for = contenedor_format_y_hora.find_all(class_= 'movie-times')
            horarios_form = []
            for hr_horario_for in horarios_for:
                btn_content_hora = hr_horario_for.find_all(class_= 'btn btn-buy')
                for btn in btn_content_hora:
                    horario_numero = btn.get_text().strip()
                    horarios_form.append(horario_numero)
                    # print(horario_numero)
                    
            # print("Nombre de la película WORKS:", nombre_pelicula)
            # print(formatos_for.get_text().strip())
            # print(horarios_form)

        # Obtener el texto completo de las funciones
        funciones_texto = [funcion.get_text() for funcion in horas_esp]

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        nombre_archivo = f"test_peliculas_cinemark_{timestamp}.docx"
        print("-" * 30)
else:
    print("No se encontró el contenedor con clase 'movies-container'")
