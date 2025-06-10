"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product
from homework.models import Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def cart():
    return Cart()

class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity) # 1000 == 1000 models.check_quantity будет True
        assert product.check_quantity(80) # 1000 > 80 models.check_quantity будет True
        assert not product.check_quantity(4000) # 1000 < 4000 models.check_quantity будет False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        quantity_on_hand = product.quantity # Начальное количество на складе
        required_quantity = 1000 # Требуемое количество товара (Если > 1000, то ValueError("Недостаточно количества товаров")
        product.buy(required_quantity) # Покупка товара с проверкой на наличие требуемого количества товара
        assert product.quantity == quantity_on_hand - required_quantity # Проверка остатка на складе

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 5)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product_in_cart(self, product, cart):
        # Добавляем товар в корзину и проверяем, что товар добавился и вернем в количестве
        cart.add_product(product, 10)
        assert cart.products[product] == 10
        assert product in cart.products.keys()

    def test_add_product_in_cart_more(self, product, cart):
        # Увеличиваем товар в корзине, проверяем, что товар добавился и увеличился в количестве при повторном обращении
        cart.add_product(product, 10)
        cart.add_product(product, 10)
        assert cart.products[product] == 20
        assert product in cart.products.keys()

    def test_remove_product_everything(self, product, cart):
        # Добавляем товар в корзину
        # Проверяем добавление товаров в корзину
        # Удаляем все товары из корзины
        # Проверяем, что корзина пустая
        cart.add_product(product, 20)
        assert product in cart.products.keys()
        cart.remove_product(product)
        assert  product not in cart.products.keys()

    def test_remove_product_partially(self, product, cart):
        # Добавляем товар в корзину
        # Проверяем добавление товаров в корзину
        # Удаляем часть товаров из корзины
        # Проверяем, что в корзине осталось
        cart.add_product(product, 25)
        assert product in cart.products.keys()
        cart.remove_product(product, 10)
        assert cart.products[product] == 15

    def test_clear_cart(self, product,cart):
        # Добавляем товар в корзину
        # Чистим корзину
        # Проверяем, что корзина пустая
        cart.add_product(product, 35)
        cart.clear()
        assert not cart.products

    def test_get_total_price(self, product,cart):
        # Добавляем товар в корзину
        # Получаем сумму и проверяем, что она больше нуля
        cart.add_product(product, 15)
        assert cart.get_total_price() > 0

    def test_buy(self, product, cart):
        # Добавляем товар в корзину
        # Покупаем товар
        cart.add_product(product, 150)
        cart.buy()
        assert not cart.products

    def test_buy_error(self, product, cart):
        # Добавляем товар в корзину в количестве больше, чем есть в наличии
        with pytest.raises(ValueError):
            cart.add_product(product,product.quantity + 5)
            cart.buy()
