import pandas as pd
import requests
from bs4 import BeautifulSoup as beauty
import sqlite3

class Scrapp():
    def __init__(self, url) -> None:
        self.url = url 
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }

       
        request = requests.get(self.url, headers=headers)

       
        if request.status_code == 200:
            self.page = beauty(request.content, 'html.parser')
            print("La página se cargó correctamente.")
        else:
            print(f"Error {request.status_code}: No se pudo acceder al contenido de la página.")

    def buscar_tablas(self):
        
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

if tablas_filtradas:
    conn = sqlite3.connect('tablas_filtradas.db')
    print("Conexión a la base de datos SQLite establecida.")

    for idx, tabla in enumerate(tablas_filtradas, start=1):
        table_name = f"tabla_{idx}"
        print(f"Guardando tabla {table_name} en la base de datos.")
        tabla.to_sql(table_name, conn, if_exists='replace', index=False)

    conn.close()
    print("Tablas guardadas exitosamente en la base de datos SQLite y conexión cerrada.")
else:
    print("No se encontraron tablas con las columnas deseadas para guardar.")
