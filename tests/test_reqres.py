import pytest
import requests
from pytest_voluptuous import S

from schemas.employee_schema import EmployeeSchema
from schemas.reqres_schema import ReqresSchema, ReqresSchemaUser, ReqresSchemaColor
from voluptuous import Schema, PREVENT_EXTRA


@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_list(path_part):
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user_schema)
        reqres_s.base_url += f'{path_part}?page=2'
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color_schema)
        reqres_s.base_url += f'{path_part}'

    responce = requests.get(reqres_s.base_url)

    assert responce.status_code == 200
    assert S(reqres_s.list_schema) == responce.json()


@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_single(path_part):
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user_schema)
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color_schema)

    # reqres_s.base_url += f'{path_part}?page=2'
    reqres_s.base_url += f'{path_part}/2'
    responce = requests.get(reqres_s.base_url)

    assert responce.status_code == 200
    assert S(reqres_s.single_schema) == responce.json()


@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_single_not_found(path_part):
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user_schema)
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color_schema)

    reqres_s.base_url += f'{path_part}/23'
    responce = requests.get(reqres_s.base_url)

    assert responce.status_code == 404
    # assert not responce.json()


def test_post():
    url = 'https://reqres.in/api/users'
    employee = {"name": "morpheus", "job": "leader"}

    responce = requests.post(url, employee)
    responce_object = EmployeeSchema()
    print(responce.json())
    assert responce.status_code == 201
    assert S(responce_object.employee_schema) == responce.json()

    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )
