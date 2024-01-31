import pytest
from data.custom_requests import CourierRequests
import allure


@allure.feature('Проверка авторизации курьера')
class TestCourierLogin:
    @allure.title('Курьер с рандомным логином может залогиниться')
    def test_courier_can_login(self, create_user_payload, make_courier_and_login):
        payload = create_user_payload(login='rand', password='1234')
        user = make_courier_and_login(data=payload)
        assert user['logged_in_courier']['id']

    @pytest.mark.parametrize("payload_schema",
                             [['rand', '1234', 'first_name']])
    @pytest.mark.parametrize("key_to_be_removed", ["login"])
    @allure.title('Курьер с отсутствующей информацией для логина не может залогиниться')
    def test_courier_cant_login_with_missing_entrance_data(self, payload_schema, key_to_be_removed,
                                                           create_user_payload, make_courier_and_login):
        payload = create_user_payload(login=payload_schema[0], password=payload_schema[1], firstname=payload_schema[2])
        user = make_courier_and_login(data=payload)
        payload.pop(key_to_be_removed)
        resp = CourierRequests().post_login_courier(data=payload, status=400)
        assert resp['message'] == 'Недостаточно данных для входа'

    @pytest.mark.parametrize("key_to_be_changed",
                             ["login",
                              "password"]
                             )
    @allure.title('Курьер с неверной парой логин-пароль не может залогиниться')
    def test_courier_cant_login_with_wrong_data(self, key_to_be_changed, create_user_payload, make_random_value):
        payload = create_user_payload(login='rand', password='rand', firstname='first_name')
        CourierRequests().post_create_courier(data=payload)
        payload[key_to_be_changed] = make_random_value
        resp = CourierRequests().post_login_courier(data=payload, status=404)
        assert resp['message'] == 'Учетная запись не найдена'

    @allure.title('Курьер, запись о котором отсутствует в БД, не может залогиниться')
    def test_courier_cant_login_for_deleted_account(self, create_user_payload):
        payload = create_user_payload(login='rand', password='rand', firstname='first_name')
        CourierRequests().post_create_courier(data=payload)
        resp = CourierRequests().post_login_courier(data=payload)
        courier_id = resp["id"]

        resp_delete = CourierRequests().delete_courier(courier_id=courier_id)
        assert resp_delete['ok']
        resp = CourierRequests().post_login_courier(data=payload, status=404)
        assert resp["message"] == "Учетная запись не найдена"
