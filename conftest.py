import pytest
from faker import Faker
import allure
from data.custom_requests import CourierRequests

fake = Faker()


@pytest.fixture
def create_user_payload():
    @allure.step('Конструируем payload для пользователя')
    def _create_user_payload(login=None, password=None, firstname=None):
        payload = {}
        if login == 'rand':
            payload["login"] = fake.name()
        elif login is not None:
            payload["login"] = login
        if password == 'rand':
            payload["password"] = fake.pyint()
        elif password is not None:
            payload["password"] = password
        if firstname == 'rand':
            payload["firstName"] = fake.name()
        elif firstname is not None:
            payload["firstName"] = firstname
        return payload

    return _create_user_payload


@pytest.fixture
@allure.step('Создаем случайное число')
def make_random_value():
    return fake.pyint()


@pytest.fixture
@allure.step('Конструируем payload для отправки заказа')
def create_order_payload():
    payload = {"firstName": fake.first_name(), "lastName": fake.last_name(),
               "address": fake.address(), "metroStation": 4, "phone": "+7 800 355 35 35", "rentTime": 5,
               "deliveryDate": "2020-06-06",
               "comment": "Saske, come back to Konoha"}
    return payload


@pytest.fixture(scope='function')
def make_courier_and_login():
    courier = {}

    def _make_courier(data):
        nonlocal courier
        created_courier = CourierRequests().post_create_courier(data=data)
        logged_in_courier = CourierRequests().post_login_courier(data=data)
        courier = {"created_courier": created_courier, "logged_in_courier": logged_in_courier}
        return courier

    yield _make_courier
    CourierRequests().delete_courier(courier_id=courier['logged_in_courier']['id'])


