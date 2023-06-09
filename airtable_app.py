import os
from dotenv import load_dotenv
import json

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

# Cargar las configuraciones desde el archivo config.json
def load_config(file_path):
    with open(file_path, 'r') as f:
        config = json.load(f)
    return config

config = load_config('config.json')

column_order = ['Fecha', 'Hora', 'Origen del dato', 'Origen', 'Referencia', 'H. salida', 'Hotel', 'Nombre invitado', 'Acompañantes', 'Sección']


def get_airtable_records(api_key, base_id, table_name, view_name):
    table = Table(api_key, base_id, table_name)
    return table.all(view=view_name)

def to_data_frame(records):
    return pd.DataFrame.from_records((r['fields'] for r in records))

def process_dataframe(df, view_type, config):
    view_fields = config['view_fields'][view_type]
    df = df.rename(columns={
        view_fields['Hora']: 'Hora',
        view_fields['Origen']: 'Origen',
        view_fields['Referencia']: 'Referencia',
        view_fields['H. salida']: 'H. salida',
        view_fields['Fecha']: 'Fecha',
        view_fields['Nombre invitado']: 'Nombre invitado'
    })
    df['Origen del dato'] = view_type
    return df

def get_combined_dataframe():
    records_llegadas = get_airtable_records(API_KEY, BASE_ID, TABLE_NAME, VIEW_NAME_LLEGADAS)
    records_salidas = get_airtable_records(API_KEY, BASE_ID, TABLE_NAME, VIEW_NAME_SALIDAS)

    llegadas_df = to_data_frame(records_llegadas)
    salidas_df = to_data_frame(records_salidas)

    llegadas_df_processed = process_dataframe(llegadas_df, 'llegada', config)
    salidas_df_processed = process_dataframe(salidas_df, 'salida', config)

    combined_df = pd.concat([llegadas_df_processed, salidas_df_processed], ignore_index=True)
    existing_columns = [col for col in column_order if col in combined_df.columns]
    combined_df = combined_df[existing_columns]

    combined_df['Fecha'] = pd.to_datetime(combined_df['Fecha'])
    combined_df = combined_df.sort_values(by=['Fecha', 'Hora'])
    combined_df['Fecha'] = combined_df['Fecha'].dt.strftime('%Y-%m-%d')

    # Reemplazar NaN con una cadena vacía
    combined_df = combined_df.fillna('')

    csv_filename = 'combined_data.csv'
    combined_df.to_csv(csv_filename, sep=';', decimal=',', index=False, encoding='utf-8-sig')

    return combined_df

def generate_html_table(df):
    html_tables = []

    # Agrupar por fecha
    grouped = df.groupby('Fecha')

    # Iterar a través de los grupos (días)
    for date, group in grouped:
        # Eliminar la columna 'Fecha'
        group = group.drop('Fecha', axis=1)

        group_table_html = group.to_html(index=False, escape=False, classes='table')
        html_tables.append(f'<h2>{date}</h2>{group_table_html}')

    return ''.join(html_tables)
