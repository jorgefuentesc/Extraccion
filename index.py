from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

chrome_driver_path = 'C:\\Users\\Jorge Fuentes\\OneDrive - Cinepolis\\Escritorio\\Extraccion\\chromedriver.exe'
website = 'https://www.cinemark.cl/cine?tag=572&cine=cinemark_mallplaza'

chrome_options = webdriver.ChromeOptions()
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(website)

time.sleep(5)
content = driver.page_source
driver.quit()

movies_data = []

soup = BeautifulSoup(content, 'html.parser')
movie_show_container = soup.find(class_='movies-container')

if movie_show_container:
    movie_boxes = movie_show_container.find_all(class_='movie-box')
    
    for movie_box in movie_boxes:
        horas_esp = movie_box.find_all(class_='movie-schedule')
        hora_peli = movie_box.find_all(class_ = 'box-movie-format')
        for peli_hora in hora_peli:
            hour = peli_hora.get_text()
            print(hour)
        titulo_peli = movie_box.find(class_ = 'movie-title')
        titulo_peli_test_a = movie_box.find('a')
        print(titulo_peli_test_a)
        print("-" * 30)
else:
    print("No se encontró el contenedor con clase 'movies-container'")
