from pathlib import Path

import requests
import settings
import yaml
from sendgrify.core import SendGrid
from user_agent import generate_user_agent

from tenempleo import utils


class TenEmpleo:
    def __init__(
        self,
        url: str = settings.TENEMPLEO_GCP_URL,
        config_filepath: str = settings.CONFIG_FILEPATH,
    ):
        self.config = self._load_config(config_filepath)
        self.job_offers = self._get_job_offers(url)
        self.matched_jobs = self._match_jobs()

    def _load_config(self, config_filepath):
        config_file = Path(config_filepath)
        return yaml.load(config_file.read_text(), Loader=yaml.FullLoader)

    def _get_job_offers(self, url):
        response = requests.get(url, headers={'User-Agent': generate_user_agent()})
        return response.json()

    def _match_jobs(self):
        matched_jobs = []
        for user in self.config['users']:
            job_offers = []
            for job_offer in self.job_offers:
                if job_offer['location'] in user['islands']:
                    if utils.is_target_job(job_offer['longText'], user['targets']):
                        job_offers.append(job_offer)
            matched_jobs.append(dict(user=user, job_offers=job_offers))
        return matched_jobs

    def notify(self):
        sg = SendGrid(
            api_key=settings.SENDGRID_APIKEY,
            from_addr=settings.NOTIFICATION_FROM_ADDR,
            from_name=settings.NOTIFICATION_FROM_NAME,
        )
        for item in self.matched_jobs:
            msg = utils.render_job_message(item)
            sg.send(
                to=item['user']['email'], subject='Ofertas de Tenempleo', msg=msg, html=True
            )
