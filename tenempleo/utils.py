import re

import markdown
import settings
from jinja2 import Template


def is_target_location(job_location: str, target_locations: list[str]):
    normalized_location = settings.LOCATION_MAPPING.get(job_location)
    if normalized_location.lower() in [i.lower() for i in target_locations]:
        return normalized_location


def is_target_job(job_text: str, targets: list[str]):
    for term in targets:
        if all([re.search(rf'\b{w}\b', job_text, re.I) for w in re.split(r'[ ,]+', term)]):
            return True
    return False


def render_job_message(item: dict):
    with open(settings.JOBS_MESSAGE_TEMPLATE) as f:
        template = Template(f.read())
    rendered_template = template.render(
        username=item['user']['name'], job_offers=item['job_offers']
    )
    return markdown.markdown(rendered_template)
