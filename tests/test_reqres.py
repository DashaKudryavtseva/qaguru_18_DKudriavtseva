'''Модуль с тестами на API запросы на форму https://reqres.in/'''
from datetime import datetime

import allure
import pytest
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
def test_get_list(reqres, path_part):
    '''Успешное получение списка объектов с помощью запроса GET.
    Тип объекта определяется параметризацией'''
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user)
        responce = reqres.get(f'{path_part}?page=2')
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color)
        responce = reqres.get(f'{path_part}')

    assert responce.status_code == 200
    assert S(reqres_s.list_schema) == responce.json()
    assert len(responce.json()['data']) == 6


@pytest.mark.get
@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_single(reqres, path_part):
    '''Успешное получение одного объекта с помощью запроса GET.
    Тип объекта определяется параметризацией'''
    if path_part == 'users':
        user = ReqresSchemaUser()
        reqres_s = ReqresSchema(data=user.user)
    elif path_part == 'unknown':
        color = ReqresSchemaColor()
        reqres_s = ReqresSchema(data=color.color)

    responce = reqres.get(f'{path_part}/2')

    assert responce.status_code == 200
    assert S(reqres_s.single_schema) == responce.json()


@pytest.mark.get
@pytest.mark.parametrize("path_part", ["users", "unknown"])
def test_get_single_not_found(reqres, path_part):
    '''Получение ошибки при попытке получить несуществующий
    объект с помощью запроса GET. Тип объекта определяется параметризацией'''
    responce = reqres.get(f'{path_part}/23')

    assert responce.status_code == 404


@pytest.mark.post
def test_post(reqres):
    '''Успешная отправка запроса на создание пользователя - POST'''
    employee = {"name": "morpheus", "job": "leader"}

    responce = reqres.post('users', employee)
    responce_object = EmployeeSchema()

    assert responce.status_code == 201
    assert S(responce_object.created) == responce.json()
    assert datetime.strptime(responce.json()['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )


@pytest.mark.put
def test_put(reqres):
    '''Успешная отправка запроса на изменение данных пользователя - PUT'''
    employee = {"name": "morpheus", "job": "zion resident"}

    responce = reqres.put('users/2', employee)
    responce_object = EmployeeSchema()

    assert responce.status_code == 200
    assert S(responce_object.updated) == responce.json()
    assert datetime.strptime(responce.json()['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )


@pytest.mark.patch
def test_patch(reqres):
    '''Успешная отправка запроса на частичное изменение данных пользователя - PATCH'''
    employee = {"name": "morpheus", "job": "zion resident"}

    responce = reqres.patch('users/2', employee)
    responce_object = EmployeeSchema()

    assert responce.status_code == 200
    assert S(responce_object.updated) == responce.json()
    assert datetime.strptime(responce.json()['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (
        responce.json()['name'] == employee['name']
        and responce.json()['job'] == employee['job']
    )


@pytest.mark.delete
def test_delete(reqres):
    '''Успешная отправка запроса на удаление пользователя - DELETE'''
    responce = reqres.delete('users/2')

    assert responce.status_code == 204


@pytest.mark.post
@pytest.mark.parametrize("path_part", ["register", "login"])
def test_register_or_login_sucsessful(reqres, path_part):
    '''Проверка успешности регистрации пользователя/входа в систему'''
    if path_part == 'register':
        register_data = {"email": "eve.holt@reqres.in", "password": "pistol"}
    elif path_part == 'login':
        register_data = {"email": "eve.holt@reqres.in", "password": "cityslicka"}

    responce = reqres.post(path_part, register_data)
    responce_object = RegisterSchema()

    assert responce.status_code == 200
    assert S(responce_object.sucsessfull) == responce.json()


@pytest.mark.post
@pytest.mark.parametrize("path_part", ["register", "login"])
def test_register_or_login_unsucsessful(reqres, path_part):
    '''Проверка получения ошибки при неверной регистрации/входа в систему'''
    if path_part == 'register':
        register_data = {"email": "sydney@fife"}
    elif path_part == 'login':
        register_data = {"email": "peter@klaven"}

    responce = reqres.post(path_part, register_data)

    assert responce.status_code == 400
    assert responce.json()['error'] == "Missing password"
