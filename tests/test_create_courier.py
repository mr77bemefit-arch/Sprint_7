import pytest
import requests
import allure
from data import Url, ResponseMessages
from helpers import order_data


class TestCreateCourier:

    @allure.title('Тест успешного создания курьера')
    def test_create_courier_success(self, generate_courier_data):

        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)

        assert response.status_code == 201
        assert response.json().get("ok") is True

        login_response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json={
                "login": generate_courier_data["login"],
                "password": generate_courier_data["password"]
            }
        )

        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")
        

    @allure.title('Тест невозможности создания двух одинаковых курьеров')
    def test_create_double_courier_mistake(self, generate_courier_data):

        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)
        response2 = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)
        
        assert response2.status_code == 409
        assert response.json()["message"] == ResponseMessages.COURIER_CREATED_MISTAKE


        login_response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json={
                "login": generate_courier_data["login"],
                "password": generate_courier_data["password"]
            }
        )

        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")
        

    #@allure.title('Тест ошибки при отсутствии одного из обязательных полей при создании курьера')
    #@pytest.mark.parametrize('missing_field', ['login', 'password'])
    #def test_create_courier_without_one_field_mistake(self, generate_courier_data, missing_field):
    #    generate_courier_data.pop(missing_field)
#
 #       response = requests.post(
  #          f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
   #         json=generate_courier_data
    #    )
#
 #       assert response.status_code == 400
  #      assert response.json()["message"] == ResponseMessages.MISSING_REQUIRED_FIELDS


    @allure.title('Тест ошибки при создании курьера с существующим логином')
    def test_create_courier_with_existing_login_mistake(self, generate_courier_data):
        requests.post(
            f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data
        )

        response = requests.post(
            f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data
        )

        assert response.status_code == 409
        assert response.json()["message"] == ResponseMessages.COURIER_CREATED_MISTAKE

        login_response = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json={
                "login": generate_courier_data["login"],
                "password": generate_courier_data["password"]
            }
        )

        assert login_response.status_code == 200

        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")


class TestLoginCourier:
    
    @allure.title('Тест успешной авторизации курьера')
    def test_login_courier_success(self, generate_courier_data):

        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)
        generate_courier_data.pop("firstName")
        response2 = requests.post(f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=generate_courier_data)

        assert response2.status_code == 200
        assert "id" in response2.json()
        
        courier_id = response2.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")
        
        

    @allure.title('Тест успешный запрос при логине возвращает id')
    def test_login_courier_success_return_id(self, generate_courier_data):

        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)
        generate_courier_data.pop("firstName")
        response2 = requests.post(f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=generate_courier_data)

        assert response2.status_code == 200
        assert "id" in response2.json()

        courier_id = response2.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")


    @allure.title('Тест ошибки при отсутствии одного из обязательных полей при логине курьера')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_without_one_field_mistake(self, generate_courier_data, missing_field):
        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)
        
        generate_courier_data.pop(missing_field)

        response2 = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=generate_courier_data
        )

        assert response2.status_code == 400
        assert response2.json()["message"] == ResponseMessages.MISSING_REQUIRED_FIELDS_LOGIN

        courier_id = response2.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")


    @allure.title('Тест ошибки при неверном логине или пароле курьера')
    @pytest.mark.parametrize('wrong_field', ['login', 'password'])
    def test_login_courier_one_field_wrong_mistake(self, generate_courier_data, wrong_field):
        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_COURIER}",
            json=generate_courier_data)
        
        generate_courier_data[wrong_field] = "wrong_value"

        response2 = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=generate_courier_data
        )

        assert response2.status_code == 404
        assert response2.json()["message"] == ResponseMessages.WRONG_FIELD_LOGIN_MISTAKE

        courier_id = response2.json().get("id")
        if courier_id:
            requests.delete(f"{Url.MAIN_URL}{Url.DELETE_COURIER}{courier_id}")
        

    @allure.title('Тест ошибки при логине не существующего курьера)')
    def test_login_courier_not_exist_wrong_mistake(self, generate_courier_data):
        
        response2 = requests.post(
            f"{Url.MAIN_URL}{Url.LOGIN_COURIER}",
            json=generate_courier_data
        )

        assert response2.status_code == 404
        assert response2.json()["message"] == ResponseMessages.WRONG_FIELD_LOGIN_MISTAKE


class TestCreateOrder:

    @allure.title('Тест успешного создания заказа')
    @pytest.mark.parametrize('scooter_color', [['BLACK'], ['GREY'], ['BLACK', 'GREY'], []])
    def test_create_order_success(self, order_data, scooter_color):
        order_data["color"] = scooter_color
               
        response = requests.post(f"{Url.MAIN_URL}{Url.CREATE_ORDER}",
            json=order_data)
        
        assert response.status_code == 201
        assert "track" in response.json()


class TestOrderList:
    
    @allure.title('Тест успешного получения списка заказов')
    def test_get_order_list_success(self):
        response = requests.get(f"{Url.MAIN_URL}{Url.CREATE_ORDER}") 
        
        assert response.status_code == 200
        assert "orders" in response.json()