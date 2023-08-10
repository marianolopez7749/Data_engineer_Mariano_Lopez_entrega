
import sqlalchemy as sa
from sqlalchemy import create_engine
import pandas as pd 
import requests
import redshift_connector
from sqlalchemy.engine.url import URL
import sqlalchemy_redshift
import traceback


def obtener_datos_desde_api(url):
    try:
        # Realizar una solicitud GET a la API
        response = requests.get(url)

        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
           
           with open("temp.csv", "wb") as f:
            f.write(response.content)

           return  "temp.csv"
                
        else:
            print(f"Error al obtener los datos. Código de estado: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error de conexión: {e}")
        return None


 
 
# URL de la API que deseas consultar
api_url = 'https://data.nasdaq.com/api/v3/datasets/WIKI/AAPL.csv'

# Llamar a la función para obtener los datos
datos_file = obtener_datos_desde_api(api_url)

if datos_file:
    try:
    
                  
        # build the sqlalchemy URL
        url = URL.create(
            drivername='redshift+redshift_connector', # indicate redshift_connector driver and dialect will be used
            host='data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com', # Amazon Redshift host
            port=5439, # Amazon Redshift port
            database='data-engineer-database', # Amazon Redshift database
            username='marianolopez7749_coderhouse', # Amazon Redshift username
            password='i7vB9sSD9B' # Amazon Redshift password
        )

        engine = sa.create_engine(url)    

        # Crear el motor de sqlalchemy para utilizar el método to_sql
        #engine = create_engine (conn_str)
    
        print('test 4')

        datos = pd.read_csv(datos_file)
        print(datos)

        # Nombre de la tabla en Redshift donde se cargarán los datos
        table_name = 'nasdaq_table'
        schema_name = 'marianolopez7749_coderhouse'

        print('test 1')

        conn = engine.connect()
        print('test 2')

        # Cargar el DataFrame en la tabla de Redshift
        datos.to_sql(
            name=table_name,
            schema=schema_name,
            con=conn,
            if_exists='replace',
            index=False
        )

        print('test 5')
        
          
        conn.close()
        
        engine.dispose()
        print("Datos cargados exitosamente en Redshift.")

    except Exception as e:
        print(f"Error al cargar los datos en Redshift: {e}")

        traceback.print_exc()  # Print the full exception traceback for debugging purposes

    finally:
        if 'conn' in locals() and conn is not None:
            try:
                
                conn.close()
                
            except Exception as e:
                print(f"Error al cerrar la conexión: {e}")
                traceback.print_exc()

        if 'engine' in locals() and engine is not None:
           engine.dispose()
else:
    print("No se pudieron obtener los datos desde la API.")
