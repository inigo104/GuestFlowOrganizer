import os
from dotenv import load_dotenv

from pyairtable import Table
import pandas as pd
from datetime import datetime

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_ID = os.getenv('BASE_ID')
TABLE_NAME = os.getenv('TABLE_NAME')
VIEW_NAME_LLEGADAS = os.getenv('VIEW_NAME_LLEGADAS')
VIEW_NAME_SALIDAS = os.getenv('VIEW_NAME_SALIDAS')

# ... (resto del código)


def get_airtable_records(api_key, base_id, table_name, view_name):
    table = Table(api_key, base_id, table_name)
    return table.all(view=view_name)

def to_data_frame_to_csv(records, filename):
    df = pd.DataFrame.from_records((r['fields'] for r in records))
    df.to_csv(f'{filename}_file.csv', sep=';', decimal=',', index=False, encoding='utf-8-sig')

def  main():
    records_llegadas = get_airtable_records(API_KEY, BASE_ID, TABLE_NAME, VIEW_NAME_LLEGADAS)
    records_salidas = get_airtable_records(API_KEY, BASE_ID, TABLE_NAME, VIEW_NAME_SALIDAS)
    to_data_frame_to_csv(records_llegadas, 'llegadas')
    to_data_frame_to_csv(records_salidas, 'salidas')


if __name__ == '__main__':
    main()