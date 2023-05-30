import os

import pytest

from utils.redefenitions import BaseSession
from dotenv import load_dotenv
from selene import browser

load_dotenv()

REQRES_URL = os.getenv('reqres_url')
WEBSHOP_URL = os.getenv('api_url')


@pytest.fixture(scope='session')
def reqres():
    reqres_session = BaseSession(base_url=REQRES_URL)
    return reqres_session


@pytest.fixture(scope='session')
def demo_web_shop_session():
    new_session = BaseSession(base_url=WEBSHOP_URL)
    browser.config.base_url = WEBSHOP_URL
    return new_session
