import settings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TenEmpleo:
    def __init__(self, url: str = settings.TENEMPLEO_URL):
        self.url = url
        self.webdriver = self._build_webdriver()
        self.page_source = self._get_page_source()
        self.job_offers = self._get_job_offers()

    def _build_webdriver(self):
        options = Options()
        options.headless = True
        return webdriver.Firefox(options=options)

    def _get_page_source(self):
        try:
            self.webdriver.get(self.url)
            WebDriverWait(self.webdriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'resize-triggers'))
            )
        except Exception as err:
            print(err)
        else:
            return self.webdriver.page_source
        finally:
            self.webdriver.quit()

    def _get_job_offers(self):
        contents = BeautifulSoup(self.page_source, 'html.parser')
        return contents
