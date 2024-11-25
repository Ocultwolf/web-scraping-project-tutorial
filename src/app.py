import os
from bs4 import BeautifulSoup as bs
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns



url = "https://ycharts.com/companies/TSLA/revenues"
respuesta = requests.get(url)

if respuesta.status_code == 200:
    
    soup = bs(respuesta.text, 'html.parser')

    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        # Obtener encabezados
        headers = [header.text.strip() for header in rows[0].find_all(['th', 'td'])]
    if headers == ["Date", "Value"]:
        print("Tabla encontrada con las columnas 'Date' y 'Value'.")

    # Iterar sobre las tablas y procesarlas
    for i, table in enumerate(tables):
        print(f"Tabla {i+1}:")
        print(table.prettify())
else:
    print(f"Error al acceder a la página: {respuesta.status_code}")
