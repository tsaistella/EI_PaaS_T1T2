# -*- coding: utf-8 -*-
import requests
import urllib3
from requests.exceptions import *

urllib3.disable_warnings()

class WebRequestManager(object):
    def __init__(self):
        pass
    @staticmethod
    def get_text(url, verify=False):
        """
        get_text
        從Web Server取得資料。

        """
        try:
            response = requests.get(url, verify=verify)
        except (HTTPError, ConnectionError) as e:
            raise e
        return response.text
    @staticmethod
    def post_json(url, data, json=True, verify=False, token=None):
        """
        post_json
        將JSON資料傳送至Web Server。

        """
        headers = {'Authorization': 'Token {}'.format(token)} if token else {}
        try:
            if json:
                response = requests.post(url, json=data, verify=verify, headers=headers)
            else:
                response = requests.post(url, data=data, verify=verify, headers=headers)
        except (HTTPError, ConnectionError) as e:
            raise e
        return response
