import pytest
import allure

from data.custom_requests import CourierRequests


@allure.feature('Проверка создания курьера')
class TestCreateCourier:
    @allure.title('Можно создать курьера со случайным логином')
    def test_can_create_courier(self, create_user_payload):
        payload = create_user_payload(login='rand', password='1234', firstname='saske')
        resp = CourierRequests().post_create_courier(data=payload)
        assert resp['ok']

    @allure.title('Нельзя создать двух курьеров с одинаковыми логинами')
    def test_cant_create_courier_dupes(self, create_user_payload):
        payload = create_user_payload(login='rand', password='1234', firstname='saske')
        CourierRequests().post_create_courier(data=payload)

        resp_dupe = CourierRequests().post_create_courier(data=payload, status=409)
        assert resp_dupe["message"] == "Этот логин уже используется. Попробуйте другой."

    @pytest.mark.parametrize("payload_schema",
                             [
                                 [None, '1234', 'first_name'],
                                 ['rand', None, 'first_name'],
                                 [None, None, 'first_name'],
                                 [None, '1234', None],
                                 ['rand', None, None]
                             ])
    @allure.title('Для создания курьера необходимо задать все обязательные поля (логин, пароль)')
    def test_all_the_fields_are_required(self, payload_schema, create_user_payload):
        payload = create_user_payload(login=payload_schema[0], password=payload_schema[1],
                                      firstname=payload_schema[2])
        resp = CourierRequests().post_create_courier(data=payload, status=400)
        assert resp["message"] == "Недостаточно данных для создания учетной записи"
