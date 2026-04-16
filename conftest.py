import pytest
import requests
import generators
from data import Url


@pytest.fixture
def generate_courier_data():
    courier_data = {
        "login": generators.courier_login_generator(),
        "password": generators.password_generator(),
        "firstName": generators.courier_firstName_generator() 
    }

    yield courier_data



