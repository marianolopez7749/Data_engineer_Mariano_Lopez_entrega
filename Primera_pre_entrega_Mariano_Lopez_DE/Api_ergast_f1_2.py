
from sqlalchemy import create_engine
import pandas as pd 
import requests
import json
import psycopg2
import gzip
import io
import binascii

def obtener_datos_desde_api(url):
    try:
        # Realizar una solicitud GET a la API
        response = requests.get(url)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            
                       
            # Check if the response is gzipped
            if response.headers.get('content-encoding') == 'gzip':
                  #Decompress the gzipped content and save it to a file
                  with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f_in:
                    with open('api_data', 'wb'):
                         
                      return 'api_data'
                
            else:
                # If not gzipped, save the content to a file directly
                with open('api_data.csv', 'wb') as f_out:
                   f_out.write(response.content)
                return 'api_data.csv'
                
        else:
            print(f"Error al obtener los datos. Código de estado: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")
        return None


 
 
# URL de la API que deseas consultar
#api_url = 'http://ergast.com/downloads/f1db.sql.gz'
api_url = 'http://ergast.com/downloads/f1db_csv.zip'

# Llamar a la función para obtener los datos
datos_file = obtener_datos_desde_api(api_url)
print(datos_file)

if datos_file:

    datos = pd.read_csv(datos_file)
    
    print(datos)

    # Print the raw content of the saved file as a hex dump
    #with open(datos_file, 'rb') as f:
        #raw_data = f.read()
        #hex_dump = binascii.hexlify(raw_data).decode('utf-8')
        #print(hex_dump)

        #df_sin_duplicados = datos_file.drop_duplicates()
    try:
    
        # Configura los detalles de la conexión a Redshift
        db_user = 'marianolopez7749_coderhouse'
        db_password = 'i7vB9sSD9B'
        db_host = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
        db_port = "5439"
        db_name = 'data-engineer-database'

        # Crea la cadena de conexión
        conn_str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        
        # Crear el motor de sqlalchemy para utilizar el método to_sql
        engine = create_engine (conn_str)
    
        # Nombre de la tabla en Redshift donde se cargarán los datos
        table_name = 'marianolopez7749_coderhouse.races_f1_2'

        # Cargar el DataFrame en la tabla de Redshift
        datos.to_sql(table_name, engine, if_exists='replace', index=False)

        print("Datos cargados exitosamente en Redshift.")

    except Exception as e:
        print(f"Error al cargar los datos en Redshift: {e}")

else:
    print("No se pudieron obtener los datos desde la API.")
    

