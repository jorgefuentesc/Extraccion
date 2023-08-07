
from bs4 import BeautifulSoup
import re
#115   111

#test comentario
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chrome_driver_path = 'C:\\Users\\Jorge Fuentes\\OneDrive - Cinepolis\\Escritorio\\Extraccion\\chromedriver.exe'


chrome_options = webdriver.ChromeOptions()
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
website = 'https://www.cinemark.cl/cine?tag=572&cine=cinemark_mallplaza'
driver.get(website)
content = driver.page_source
driver.quit()

print(content)
