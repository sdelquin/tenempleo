from pathlib import Path

import requests
import settings
import yaml
from user_agent import generate_user_agent

from tenempleo import utils


class TenEmpleo:
    def __init__(
        self,
        url: str = settings.TENEMPLEO_GCP_URL,
        config_filepath: str = settings.CONFIG_FILEPATH,
    ):
        self.config = self._load_config(config_filepath)
        self.contents = self._get_contents(url)
        self.job_offers = self._prepare_job_offers()

    def _load_config(self, config_filepath):
        config_file = Path(config_filepath)
        return yaml.load(config_file.read_text(), Loader=yaml.FullLoader)

    def _get_contents(self, url):
        response = requests.get(url, headers={'User-Agent': generate_user_agent()})
        return response.json()

    def _prepare_job_offers(self):
        job_offers = []
        for user in self.config['users']:
            for job_offer in self.contents:
                if job_offer['location'] in user['islands']:
                    if utils.is_target_job(job_offer['longText'], user['targets']):
                        job_offers.append(dict(user=user, job_offer=job_offer))
        return job_offers
