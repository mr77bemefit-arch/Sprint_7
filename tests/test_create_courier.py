import pytest
import requests
import allure
from data import Url, ResponseMessages, OrderData


class TestCreateCourier:

    @allure.title('Тест успешного создания курьера')
    def test_create_courier_success(self, created_courier):
        response = created_courier["create_response"]

        assert response.status_code == 201
        assert response.json().get("ok") is True

    @allure.title('Тест невозможности создания двух одинаковых курьеров')
    def test_create_double_courier_mistake(self, created_courier, create_courier):
        courier_data = created_courier["courier_data"]

        response = create_courier(courier_data)

        assert response.status_code == 409
        assert response.json()["message"] == ResponseMessages.COURIER_CREATED_MISTAKE

    @allure.title('Тест ошибки при отсутствии одного из обязательных полей при создании курьера')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_without_one_field_mistake(self, generate_courier_data, missing_field, create_courier):
        generate_courier_data.pop(missing_field)

        response = create_courier(generate_courier_data)

        assert response.status_code == 400
        assert response.json()["message"] == ResponseMessages.MISSING_REQUIRED_FIELDS

    @allure.title('Тест ошибки при создании курьера с существующим логином')
    def test_create_courier_with_existing_login_mistake(self, created_courier, create_courier):
        courier_data = created_courier["courier_data"]

        response = create_courier(courier_data)

        assert response.status_code == 409
        assert response.json()["message"] == ResponseMessages.COURIER_CREATED_MISTAKE

class TestLoginCourier:

    @allure.title('Тест успешной авторизации курьера')
    def test_login_courier_success(self, created_courier, login_courier):
        courier_data = created_courier["courier_data"]

        response = login_courier({
            "login": courier_data["login"],
            "password": courier_data["password"]
        })

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Тест: успешный запрос при логине возвращает id')
    def test_login_courier_success_return_id(self, created_courier, login_courier):
        courier_data = created_courier["courier_data"]

        response = login_courier({
            "login": courier_data["login"],
            "password": courier_data["password"]
        })

        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title('Тест ошибки при отсутствии одного из обязательных полей при логине курьера')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_without_one_field_mistake(self, created_courier, login_courier, missing_field):
        courier_data = created_courier["courier_data"]

        login_data = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        login_data.pop(missing_field)

        response = login_courier(login_data)

        assert response.status_code == 400
        assert response.json()["message"] == ResponseMessages.MISSING_REQUIRED_FIELDS_LOGIN

    @allure.title('Тест ошибки при неверном логине или пароле курьера')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_courier_one_field_wrong_mistake(self, created_courier, login_courier, wrong_field):
        courier_data = created_courier["courier_data"]

        login_data = {
            "login": courier_data["login"],
            "password": courier_data["password"]
        }
        login_data[wrong_field] = "wrong_value"

        response = login_courier(login_data)

        assert response.status_code == 404
        assert response.json()["message"] == ResponseMessages.WRONG_FIELD_LOGIN_MISTAKE

    @allure.title('Тест ошибки при логине несуществующего курьера')
    def test_login_courier_not_exist_wrong_mistake(self, generate_courier_data, login_courier):
        response = login_courier({
            "login": generate_courier_data["login"],
            "password": generate_courier_data["password"]
        })

        assert response.status_code == 404
        assert response.json()["message"] == ResponseMessages.WRONG_FIELD_LOGIN_MISTAKE

class TestCreateOrder:

    @allure.step('Создать заказ')
    def create_order(self, order_data):
        return requests.post(
            f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
            json=order_data
        )

    @allure.title('Тест успешного создания заказа')
    @pytest.mark.parametrize('scooter_color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_create_order_success(self, scooter_color):
        order_data = OrderData.generate_order_data.copy()
        order_data["color"] = scooter_color

        response = self.create_order(order_data)

        assert response.status_code == 201
        assert "track" in response.json()


class TestOrderList:

    @allure.step('Получить список заказов')
    def get_order_list(self):
        return requests.get(f"{Url.MAIN_URL}{Url.CREATE_ORDER}")

    @allure.title('Тест успешного получения списка заказов')
    def test_get_order_list_success(self):
        response = self.get_order_list()

        assert response.status_code == 200
        assert "orders" in response.json()

