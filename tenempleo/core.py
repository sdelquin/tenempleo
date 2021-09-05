from pathlib import Path

import redis
import requests
import settings
import yaml
from logzero import logger
from sendgrify.core import SendGrid
from user_agent import generate_user_agent

from tenempleo import utils


class TenEmpleo:
    def __init__(
        self,
        url: str = settings.TENEMPLEO_GCP_URL,
        config_filepath: str = settings.CONFIG_FILEPATH,
    ):
        logger.debug('Connecting to redis...')
        self.redis = redis.Redis(db=settings.REDIS_DB)
        self.config = self._load_config(config_filepath)
        self.job_offers = self._get_job_offers(url)
        self.matched_jobs = self._match_jobs()

    def _load_config(self, config_filepath):
        logger.info(f'Loading yaml config file from {config_filepath}...')
        config_file = Path(config_filepath)
        return yaml.load(config_file.read_text(), Loader=yaml.FullLoader)

    def _get_job_offers(self, url):
        logger.info(f'Requesting data from {url} ...')
        response = requests.get(url, headers={'User-Agent': generate_user_agent()})
        return response.json()

    def _is_eligible_job(self, user, job_offer):
        return all(
            [
                utils.is_target_location(job_offer['location'], user['locations']),
                utils.is_target_job(job_offer['longText'], user['targets']),
                self.redis.get(user['email'] + str(job_offer['id'])) is None,
            ]
        )

    def _match_jobs(self):
        matched_jobs = []
        for user in self.config['users']:
            username = user['name']
            logger.debug(f'{username}: Matching job offers...')
            job_offers = []
            for job_offer in self.job_offers:
                if self._is_eligible_job(user, job_offer):
                    logger.debug(f'{job_offer["shortText"]} ({job_offer["id"]})')
                    logger.debug(
                        f'{username}: ↑ Match! Appending to eligible job offers...'
                    )
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
            username = item["user"]["name"]
            logger.debug(f'{username}: Notifying user...')
            if len(item['job_offers']) == 0:
                logger.debug(f'{username}: No job offers found. Skipped!')
                continue
            msg = utils.render_job_message(item)
            user_email = item['user']['email']
            logger.debug(f'{username}: Sending email to {user_email}...')
            sg.send(to=user_email, subject='Ofertas de Tenempleo', msg=msg, html=True)
            # update delivered job offers
            logger.debug('Updating delivered job offers on redis...')
            for job_offer in item['job_offers']:
                self.redis.set(user_email + str(job_offer['id']), 1)
