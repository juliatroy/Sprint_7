import pytest
import allure

from data.custom_requests import OrderRequests


@allure.title('Проверка создания и выгрузки заказов')
class TestOrderOptions:
    @allure.description('Можно создать заказ с цветом {color}, ответ содержит "track"')
    @pytest.mark.parametrize('color', [
        ['BLACK'],
        ['GREY'],
        ['BLACK', 'GREY'],
        None])
    def test_create_order_successful(self, color, create_order_payload):
        payload = create_order_payload
        if color is not None:
            payload["color"] = color
        print(payload)
        resp = OrderRequests().post_create_order(data=payload)
        assert "track" in resp.keys()

    @allure.description('Ручка получения списка заказов возвращает список заказов, ответ содержит "orders"')
    def test_get_order_returns_json(self):
        resp = OrderRequests().get_orders_list()
        assert "orders" in resp.keys()
