import requests
import settings
from user_agent import generate_user_agent


class TenEmpleo:
    def __init__(self, url: str = settings.TENEMPLEO_GCP_URL):
        self.url = url
        self.contents = self._get_contents()

    def _get_contents(self):
        response = requests.get(self.url, headers={'User-Agent': generate_user_agent()})
        return response.json()
