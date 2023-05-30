import logging

import allure
import curlify as curlify
from allure import attachment_type
from requests import Session
from allure import step


class BaseSession(Session):
    def __init__(self, **kwargs):
        self.base_url = kwargs.pop('base_url')
        super().__init__()

    def request(self, method, url, **kwargs):
        with step(f'{method} in {url}'):
            responce = super().request(method, url=f'{self.base_url}{url}', **kwargs)
            content_type = responce.headers.get('content-type')
            curl = curlify.to_curl(responce.request)
            curl_log = f'Status code: {responce.status_code} {curl}'

            if content_type is None:
                logging.info('There is no content on the sent request.')
            elif 'text' in content_type:
                logging.info(f'Content: \n{responce.text}')
            elif 'json' in content_type:
                logging.info(f'Content: \n{responce.json()}')

            logging.info(curl)
            allure.attach(
                curl_log, name='Curl Log', attachment_type=attachment_type.TEXT
            )
            allure.attach(
                responce.text, name='Response', attachment_type=attachment_type.TEXT
            )

        return responce
