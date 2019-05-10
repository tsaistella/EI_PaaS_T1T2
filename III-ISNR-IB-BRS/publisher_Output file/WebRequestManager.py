import requests
import urllib3
from requests.exceptions import *

urllib3.disable_warnings()

class WebRequestManager(object):
    def __init__(self):
        pass
    @staticmethod
    def get_text(url, verify=False):
        try:
            response = requests.get(url, verify=verify)
        except (HTTPError, ConnectionError) as e:
            raise e
        return response.text
