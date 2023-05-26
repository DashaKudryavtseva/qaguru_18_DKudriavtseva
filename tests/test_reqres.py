from datetime import datetime

import pytest
import requests
from pytest_voluptuous import S

from reqres_schemas.employees import EmployeeSchema
from reqres_schemas.main_type import (
    ReqresSchema,
    ReqresSchemaUser,
    ReqresSchemaColor,
)

from reqres_schemas.registers import RegisterSchema


@pytest.mark.get
@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_list(presets, path_part):
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user)
        url = f'{presets}{path_part}?page=2'
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color)
        url = f'{presets}{path_part}'

    responce = requests.get(url)

    assert responce.status_code == 200
    assert S(reqres_s.list_schema) == responce.json()
    assert len(responce.json()['data']) == 6


@pytest.mark.get
@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_single(presets, path_part):
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user)
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color)

    url = f'{presets}{path_part}/2'
    responce = requests.get(url)

    assert responce.status_code == 200
    assert S(reqres_s.single_schema) == responce.json()


@pytest.mark.get
@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_single_not_found(presets, path_part):
    url = f'{presets}{path_part}/23'

    responce = requests.get(url)

    assert responce.status_code == 404


@pytest.mark.post
def test_post(presets):
    url = f'{presets}users'
    employee = {"name": "morpheus", "job": "leader"}

    responce = requests.post(url, employee)
    responce_object = EmployeeSchema()

    assert responce.status_code == 201
    assert S(responce_object.created) == responce.json()
    assert datetime.strptime(responce.json()['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )


@pytest.mark.put
def test_put(presets):
    url = f'{presets}users/2'
    employee = {"name": "morpheus", "job": "zion resident"}

    responce = requests.put(url, employee)
    responce_object = EmployeeSchema()

    assert responce.status_code == 200
    assert S(responce_object.updated) == responce.json()
    assert datetime.strptime(responce.json()['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )


@pytest.mark.patch
def test_patch(presets):
    url = f'{presets}users/2'
    employee = {"name": "morpheus", "job": "zion resident"}

    responce = requests.patch(url, employee)
    responce_object = EmployeeSchema()

    assert responce.status_code == 200
    assert S(responce_object.updated) == responce.json()
    assert datetime.strptime(responce.json()['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )


@pytest.mark.delete
def test_delete(presets):
    url = f'{presets}users/2'

    responce = requests.delete(url)

    assert responce.status_code == 204


@pytest.mark.post
@pytest.mark.parametrize("path_part", ["register", "login"])
def test_register_or_login_sucsessful(presets, path_part):
    url = f'{presets}{path_part}'
    if path_part == 'register':
        register_data = {"email": "eve.holt@reqres.in", "password": "pistol"}
    elif path_part == 'login':
        register_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}

    responce = requests.post(url, register_data)
    responce_object = RegisterSchema()

    assert responce.status_code == 200
    assert S(responce_object.sucsessfull) == responce.json()


@pytest.mark.post
@pytest.mark.parametrize("path_part", ["register", "login"])
def test_register_or_login_unsucsessful(presets, path_part):
    url = f'{presets}{path_part}'
    if path_part == 'register':
        register_data = {"email": "sydney@fife"}
    elif path_part == 'login':
        register_data = {"email": "peter@klaven"}

    responce = requests.post(url, register_data)

    assert responce.status_code == 400
    assert responce.json()['error'] == "Missing password"
