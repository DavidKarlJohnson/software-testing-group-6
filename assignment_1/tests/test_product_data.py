import pytest
from assignment_1.online_shopping_cart.product import product_data
from assignment_1.online_shopping_cart.product.product import Product


# 10 tests for get_products using monkeypatch to avoid reading real files

def test_get_products_single_valid(monkeypatch):
    data = [
        {'Product': 'Widget', 'Price': '9.99', 'Units': '5'}
    ]

    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    products = product_data.get_products(file_name='dummy.csv')
    assert isinstance(products, list)
    assert len(products) == 1
    p = products[0]
    assert isinstance(p, Product)
    assert p.name == 'Widget'
    assert p.price == pytest.approx(9.99)
    assert p.units == 5


def test_get_products_multiple(monkeypatch):
    data = [
        {'Product': 'A', 'Price': '1.0', 'Units': '1'},
        {'Product': 'B', 'Price': '2.5', 'Units': '10'},
        {'Product': 'C', 'Price': '0.0', 'Units': '0'},
    ]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    products = product_data.get_products()
    assert [p.name for p in products] == ['A', 'B', 'C']
    assert products[1].price == pytest.approx(2.5)
    assert products[2].units == 0


def test_get_products_price_decimal(monkeypatch):
    data = [{'Product': 'X', 'Price': '123.456', 'Units': '2'}]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    p = product_data.get_products()[0]
    assert p.price == pytest.approx(123.456)


def test_get_products_zero_units(monkeypatch):
    data = [{'Product': 'Y', 'Price': '5', 'Units': '0'}]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    p = product_data.get_products()[0]
    assert p.units == 0


def test_get_products_negative_units(monkeypatch):
    # The function converts strings to int; negative values will be preserved
    data = [{'Product': 'Z', 'Price': '1.23', 'Units': '-3'}]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    p = product_data.get_products()[0]
    assert p.units == -3


def test_get_products_missing_field_raises(monkeypatch):
    data = [{'Product': 'NoPrice', 'Units': '1'}]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    with pytest.raises(KeyError):
        product_data.get_products()


def test_get_products_non_numeric_price_raises(monkeypatch):
    data = [{'Product': 'BadPrice', 'Price': 'abc', 'Units': '1'}]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    with pytest.raises(ValueError):
        product_data.get_products()


def test_get_products_non_integer_units_raises(monkeypatch):
    data = [{'Product': 'BadUnits', 'Price': '1.0', 'Units': '2.5'}]
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    with pytest.raises(ValueError):
        product_data.get_products()


def test_get_products_empty_list(monkeypatch):
    data: list[dict] = []
    monkeypatch.setattr(product_data, 'get_csv_data', lambda csv_filename, is_dict: data)
    products = product_data.get_products()
    assert products == []


def test_get_products_passes_filename(monkeypatch):
    # Ensure the provided file_name is passed through to the csv reader function
    called = {}

    def fake_get_csv(csv_filename, is_dict):
        called['name'] = csv_filename
        return [{'Product': 'P', 'Price': '1', 'Units': '1'}]

    monkeypatch.setattr(product_data, 'get_csv_data', fake_get_csv)
    product_data.get_products(file_name='myfile.csv')
    assert called.get('name') == 'myfile.csv'