import json
import requests
import allure
from faker import Faker

fake = Faker()


class BaseRequests:
    host = 'https://qa-scooter.praktikum-services.ru'

    def exec_post_request_and_check(self, url, data, status):
        response = requests.post(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def exec_delete_request_and_check(self, url, data, status):
        response = requests.delete(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def exec_get_request_and_check(self, url, status):
        response = requests.get(url=url)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def exec_put_request_and_check(self, url, data, status):
        response = requests.put(url=url, data=data)
        assert response.status_code == status
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text


class CourierRequests(BaseRequests):
    courier_handler = '/api/v1/courier'
    courier_login_handler = '/api/v1/courier/login'

    @allure.step('Создаем курьера, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_create_courier(self, data=None, status=201):
        url = f"{self.host}{self.courier_handler}"
        return self.exec_post_request_and_check(url, data=data, status=status)

    @allure.step('Логиним курьера, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_login_courier(self, data=None, status=200):
        url = f"{self.host}{self.courier_login_handler}"
        return self.exec_post_request_and_check(url, data=data, status=status)

    @allure.step('Удаляем курьера, отправив запрос DELETE. Ожидаем статус респонса {status}')
    def delete_courier(self, courier_id=None, status=200):
        url = f"{self.host}{self.courier_handler}/{courier_id}"
        delete_payload = {"id": courier_id}
        return self.exec_delete_request_and_check(url, data=delete_payload, status=status)


class OrderRequests(BaseRequests):
    order_handler = '/api/v1/orders'

    @allure.step('Создаем заказ, отправив запрос POST. Ожидаем статус респонса {status}')
    def post_create_order(self, data=None, status=201):
        url = f"{self.host}{self.order_handler}"
        return self.exec_post_request_and_check(url, data=json.dumps(data), status=status)

    @allure.step('Получаем список заказов, отправив запрос GET. Ожидаем статус респонса {status}')
    def get_orders_list(self, status=200):
        url = f"{self.host}{self.order_handler}"
        return self.exec_get_request_and_check(url, status=status)

