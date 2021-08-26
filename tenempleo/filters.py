import datetime

import settings


def format_location(value):
    return settings.LOCATION_MAPPING.get(value, 'No disponible')


def format_date(value):
    date = datetime.datetime.strptime(value, '%a %b %d %H:%M:%S %z %Y')
    return date.strftime('%d/%m/%y · %H:%Mh %Z')
