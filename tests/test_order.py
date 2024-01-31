import pytest
import allure

from data.custom_requests import OrderRequests


@allure.feature('Проверка создания и выгрузки заказов')
class TestOrderOptions:
    @allure.title('Можно создать заказ с цветом {color}, ответ содержит "track"')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY']])
    def test_create_order_successful(self, color, create_order_payload):
        payload = create_order_payload
        payload["color"] = color
        resp = OrderRequests().post_create_order(data=payload)
        assert "track" in resp.keys()

    @allure.title('Можно создать заказ без цвета, ответ содержит "track"')
    def test_create_order_with_no_color_successful(self, create_order_payload):
        payload = create_order_payload
        resp = OrderRequests().post_create_order(data=payload)
        assert "track" in resp.keys()

    @allure.title('Ручка получения списка заказов возвращает список заказов, ответ содержит "orders"')
    def test_get_order_returns_json(self):
        resp = OrderRequests().get_orders_list()
        assert "orders" in resp.keys()
