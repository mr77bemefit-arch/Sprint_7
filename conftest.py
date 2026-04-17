import pytest
import requests
import generators
import allure
from data import Url


@pytest.fixture
def generate_courier_data():
    courier_data = {
        "login": generators.courier_login_generator(),
        "password": generators.password_generator(),
        "firstName": generators.courier_firstName_generator()
    }
    yield courier_data


@pytest.fixture
def create_courier():
    @allure.step('Создать курьера')
    def _create_courier(courier_data):
        return requests.post(
            f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=courier_data
        )
    return _create_courier


@pytest.fixture
def created_courier(generate_courier_data, create_courier):
    with allure.step('Создать курьера'):
        create_response = create_courier(generate_courier_data)

    with allure.step('Авторизовать курьера'):
        login_response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json={
                "login": generate_courier_data["login"],
                "password": generate_courier_data["password"]
            }
        )
        courier_id = login_response.json().get("id")

    yield {
        "courier_data": generate_courier_data,
        "create_response": create_response,
        "courier_id": courier_id
    }

    if courier_id:
        with allure.step('Удалить курьера'):
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")

@pytest.fixture
def login_courier():
    @allure.step('Авторизовать курьера')
    def _login_courier(login_data):
        return requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=login_data
        )
    return _login_courier

