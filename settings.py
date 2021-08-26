from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.stem
TEMPLATES_DIR = PROJECT_DIR / 'templates'

TENEMPLEO_GCP_URL = config('TENEMPLEO_GCP_URL')
CONFIG_FILEPATH = config('CONFIG_FILEPATH', default='config.yml')

SENDGRID_APIKEY = config('SENDGRID_APIKEY')
NOTIFICATION_FROM_ADDR = config('NOTIFICATION_FROM_ADDR')
NOTIFICATION_FROM_NAME = config('NOTIFICATION_FROM_NAME')

JOBS_MESSAGE_TEMPLATE = config('JOBS_MESSAGE_TEMPLATE', default='jobs.md')

LOCATION_MAPPING = {
    'canarias': 'Canarias',
    'elhierro': 'El Hierro',
    'fuerteventura': 'Fuerteventura',
    'grancanaria': 'Gran Canaria',
    'lagomera': 'La Gomera',
    'lagraciosa': 'La Graciosa',
    'lanzarote': 'Lanzarote',
    'lapalma': 'La Palma',
    'tenerife': 'Tenerife',
}

REDIS_DB = config('REDIS_DB', default=0, cast=int)
