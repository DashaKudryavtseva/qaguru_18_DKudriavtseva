import os

from allure import step
from selene import browser, have
from dotenv import load_dotenv

load_dotenv()

LOGIN = os.getenv('user_login')
PASSWORD = os.getenv('user_password')


def test_login(demo_web_shop_session):
    """Successful authorization to some demowebshop (UI)"""
    with step("Open login page"):
        browser.open("/login")

    with step("Fill login form"):
        browser.element("#Email").send_keys(LOGIN)
        browser.element("#Password").send_keys(PASSWORD).press_enter()

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))


def test_login_through_api(demo_web_shop_session):
    """Successful authorization to some demowebshop (UI)"""
    with step("Login through API"):
        response = demo_web_shop_session.post(
            url='/login',
            params={'Email': LOGIN, 'Password': PASSWORD},
            headers={
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
            },
            allow_redirects=False,
        )
        authorization_cookie = response.cookies.get('NOPCOMMERCE.AUTH')

    with step("Open image 'logo.png'"):
        browser.open("/Themes/DefaultClean/Content/images/logo.png")

    with step("Add cookie and open page"):
        browser.driver.add_cookie(
            {"name": "NOPCOMMERCE.AUTH", "value": authorization_cookie}
        )
        browser.open("")

    with step("Verify successful authorization"):
        browser.element(".account").should(have.text(LOGIN))
