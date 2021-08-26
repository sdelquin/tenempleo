from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).resolve().parent
PROJECT_NAME = PROJECT_DIR.stem

TENEMPLEO_GCP_URL = config('TENEMPLEO_GCP_URL')
CONFIG_FILEPATH = config('CONFIG_FILEPATH', default='config.yml')
SENDGRID_APIKEY = config('SENDGRID_APIKEY')
NOTIFICATION_FROM_ADDR = config('NOTIFICATION_FROM_ADDR')
NOTIFICATION_FROM_NAME = config('NOTIFICATION_FROM_NAME')
JOBS_MESSAGE_TEMPLATE = config(
    'JOBS_MESSAGE_TEMPLATE', default=PROJECT_DIR / PROJECT_NAME / 'jobs.md'
)
