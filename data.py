class Url:
    MAIN_URL = "https://qa-scooter.praktikum-services.ru"
    CREATE_COURIER = "/api/v1/courier"
    LOGIN_COURIER = "/api/v1/courier/login"
    DELETE_COURIER = "/api/v1/courier/"
    CREATE_ORDER = "/api/v1/orders"
    
    
class ResponseMessages:
    COURIER_CREATED_MISTAKE = "Этот логин уже используется"
    MISSING_REQUIRED_FIELDS = "Недостаточно данных для создания учетной записи"
    MISSING_REQUIRED_FIELDS_LOGIN = "Недостаточно данных для входа"
    WRONG_FIELD_LOGIN_MISTAKE = "Учетная запись не найдена"

class OrderData:
    generate_order_data = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 38",
    "rentTime": 5,
    "deliveryDate": "2026-06-06",
    "comment": "Saske, come back to Konoha",
    "color": []}


