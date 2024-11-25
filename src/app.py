import pandas as pd
import requests
from bs4 import BeautifulSoup as beauty

class Scrapp():
    def __init__(self, url):
        self.url = url 
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }

        # Realizar la solicitud HTTP con headers
        request = requests.get(self.url, headers=headers)

        # Verificar el estado de la respuesta
        if request.status_code == 200:
            self.page = beauty(request.content, 'html.parser')
            print("La página se cargó correctamente.")
        else:
            print(f"Error {request.status_code}: No se pudo acceder al contenido de la página.")

    def buscar_tablas(self):
        # Verificar si hay tablas en el contenido
        tables = self.page.find_all('table')
        if tables:
            print(f"Se encontraron {len(tables)} tablas en la página.")
            dataframes = []

            for table in tables:

                rows = table.find_all('tr')
                table_data = []

                for row in rows:

                    cols = row.find_all(['th', 'td'])
                    table_data.append([col.text.strip() for col in cols])

                if len(table_data) > 1:  
                    df = pd.DataFrame(table_data[1:], columns=table_data[0])  
                    dataframes.append(df)

            return dataframes
        else:
            print("No se encontraron tablas en la página.")
            return []


buscador = Scrapp(url='https://ycharts.com/companies/TSLA/revenues')
buscador_tablas = buscador.buscar_tablas()

columnas_deseadas = ['Date', 'Value']
tablas_filtradas = []

for idx, tabla in enumerate(buscador_tablas, start=1):
    columnas_tabla = tabla.columns.tolist()
    print(f"Tabla {idx} columnas: {columnas_tabla}")
    
    if all(col in columnas_tabla for col in columnas_deseadas):
        print(f"Tabla {idx} coincide con las columnas deseadas.")
        tablas_filtradas.append(tabla)

# Mostrar las tablas filtradas
if tablas_filtradas:
    print(f"Se encontraron {len(tablas_filtradas)} tablas con las columnas deseadas:")
    for idx, tabla in enumerate(tablas_filtradas, start=1):
        print(f"Tabla {idx}:\n{tabla.head()}")
else:
    print("No se encontraron tablas con las columnas deseadas.")
