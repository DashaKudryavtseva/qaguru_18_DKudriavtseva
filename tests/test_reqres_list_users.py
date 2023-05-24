import requests
from voluptuous import Schema, PREVENT_EXTRA
from pytest_voluptuous import S


def test_get_users_page_number():
    url = 'https://reqres.in/api/users?page=2'

    responce = requests.get(url)

    assert responce.status_code == 200
    assert responce.json()['page'] == 2


def test_get_users_on_page():
    url = 'https://reqres.in/api/users?page=2'

    responce = requests.get(url)
    per_page = responce.json()['per_page']
    data = responce.json()['data']

    assert per_page == 6


def test_get_users_validate_schema():
    url = 'https://reqres.in/api/users?page=2'

    responce = requests.get(url)
    per_page = responce.json()['per_page']
    data = responce.json()['data']
    user_schema = Schema(
        {
            "id": int,
            "email": str,
            "first_name": str,
            "last_name": str,
            "avatar": str,
        },
        extra=PREVENT_EXTRA,
        required=True,
    )

    list_users_schema = Schema(
        {
            "page": int,
            "per_page": int,
            "total": int,
            "total_pages": int,
            "data": [user_schema],
            "support": {
                "url": str,
                "text": str,
            },
        },
        extra=PREVENT_EXTRA,
        required=True,
    )

    assert S(list_users_schema) == responce.json()
