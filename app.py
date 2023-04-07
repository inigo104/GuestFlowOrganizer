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

# ... (resto del código)
