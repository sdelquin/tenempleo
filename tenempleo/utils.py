import re

import jinja2
import logzero
import markdown
import settings

from tenempleo import filters


def init_logger():
    console_logformat = (
        '%(asctime)s '
        '%(color)s'
        '[%(levelname)-8s] '
        '%(end_color)s '
        '%(message)s '
        '%(color)s'
        '(%(filename)s:%(lineno)d)'
        '%(end_color)s'
    )
    # remove colors on logfile
    file_logformat = re.sub(r'%\((end_)?color\)s', '', console_logformat)

    console_formatter = logzero.LogFormatter(fmt=console_logformat)
    file_formatter = logzero.LogFormatter(fmt=file_logformat)
    logzero.setup_default_logger(formatter=console_formatter)
    logzero.logfile(
        settings.LOGFILE,
        maxBytes=settings.LOGFILE_SIZE,
        backupCount=settings.LOGFILE_BACKUP_COUNT,
        formatter=file_formatter,
    )
    return logzero.logger


def is_target_location(job_location: str, target_locations: list[str]):
    normalized_location = settings.LOCATION_MAPPING.get(job_location)
    return normalized_location.lower() in [i.lower() for i in target_locations]


def is_target_job(job_text: str, targets: list[str]):
    for term in targets:
        if all([re.search(rf'\b{w}\b', job_text, re.I) for w in re.split(r'[ ,]+', term)]):
            return True
    return False


def init_jinja():
    loader = jinja2.FileSystemLoader(settings.TEMPLATES_DIR)
    env = jinja2.Environment(loader=loader)
    env.filters['format_date'] = filters.format_date
    env.filters['format_location'] = filters.format_location
    return env


def render_job_message(item: dict):
    jinja_env = init_jinja()
    template = jinja_env.get_template(settings.JOBS_MESSAGE_TEMPLATE)
    rendered_template = template.render(
        username=item['user']['name'], job_offers=item['job_offers']
    )
    return markdown.markdown(rendered_template)
