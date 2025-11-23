import json
import os
import tempfile
import pytest

from assignment_1.online_shopping_cart.checkout.shopping_cart import ShoppingCart
from assignment_1.online_shopping_cart.product.product import Product

# ----- TASK 3.4 -----
# TODO: Write 15 test cases for the function 'checkout_and_payment' located in  /online_shopping_cart/checkout/checkout_process.py
# NOTE: Complete the following task before the tests: "Modify the checkout_and_payment function to update the "wallet" information in the users.json file."


# Fixture for temporary JSON file to be used in tests
@pytest.fixture
def temp_json():
    data = [{"username": "Ramanathan",
            "password": "Notaproblem23*",
            "wallet": 100.0
            },
             {
            "username": "Samantha",
            "password": "SecurePass123/^",
            "wallet": 150.0
             },
             {
            "username": "Maximus",
            "password": "StrongPwd!23",
            "wallet": 75.0
    }]
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_json:
        json.dump(data, tmp_json)
        tmp_json.flush()
        yield tmp_json.name

    os.remove(tmp_json.name)


# Use this function for patching the return value of the function 'get_products',
# which reads the products.csv file
def mock_global_products():
    return [Product(name='Apple', price=2.0, units=10),
            Product(name='Banana', price=1.0, units=15),
            Product(name='Orange', price=1.5, units=8),
            Product(name='Grapes', price=3.0, units=1),
            Product(name='Strawberry', price=4.0, units=12)]


# Test 1: Add the first product (1) within the acceptable bounds [1,5]
def test_add_product_within_bounds_lower(mocker, capsys):
    login_info = {'username': 'Maximus', 'wallet': 1000.0}
    mocker.patch('assignment_1.online_shopping_cart.product.product_data.get_products', return_value=mock_global_products())
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=['1', 'l', 'y'])
    mocker.patch('builtins.exit', side_effect=SystemExit)

    # NOTE: Global variable 'global_products' is set at module import of this test file.
    #       The import below is to update this variable to the patch set within this test.
    from assignment_1.online_shopping_cart.checkout import checkout_process
    checkout_process.global_cart = ShoppingCart()
    with pytest.raises(SystemExit):
        checkout_process.checkout_and_payment(login_info)

    assert capsys.readouterr().out == 'Apple added to your cart.\n''Your cart is not empty. You have the following items:\n''Apple - $2.0 - Units: 1\n''You have been logged out.\n'


# Test 2: Add the last product (5) within the acceptable bounds [1,5]
def test_add_product_within_bounds_upper(mocker, capsys):
    login_info = {'username': 'Maximus', 'wallet': 1000.0}
    mocker.patch('assignment_1.online_shopping_cart.product.product_data.get_products', return_value=mock_global_products())
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=['5', 'l', 'y'])
    mocker.patch('builtins.exit', side_effect=SystemExit)

    # NOTE: Global variable 'global_products' is set at module import of this test file.
    #       The import below is to update this variable to the patch set within this test.
    from assignment_1.online_shopping_cart.checkout import checkout_process
    checkout_process.global_cart = ShoppingCart()
    with pytest.raises(SystemExit):
        checkout_process.checkout_and_payment(login_info)

    assert capsys.readouterr().out == 'Strawberry added to your cart.\n''Your cart is not empty. You have the following items:\n''Strawberry - $4.0 - Units: 1\n''You have been logged out.\n'


# Test 3: Add a product (6) that's out of bounds [1,5]
def test_add_product_out_of_bounds_upper(mocker, capsys):
    login_info = {'username': 'Maximus', 'wallet': 1000.0}
    mocker.patch('assignment_1.online_shopping_cart.product.product_data.get_products', return_value=mock_global_products())
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=['6', 'l', 'y'])
    mocker.patch('builtins.exit', side_effect=SystemExit)

    # NOTE: Global variable 'global_products' is set at module import of this test file.
    #       The import below is to update this variable to the patch set within this test.
    from assignment_1.online_shopping_cart.checkout import checkout_process
    checkout_process.global_cart = ShoppingCart()
    with pytest.raises(SystemExit):
        checkout_process.checkout_and_payment(login_info)

    assert capsys.readouterr().out == 'Invalid input. Please try again.\nYou have been logged out.\n'


# Test 4: Add a product (0) that's out of bounds [1,5]
def test_add_product_out_of_bounds_lower(mocker, capsys):
    login_info = {'username': 'Maximus', 'wallet': 1000.0}
    mocker.patch('assignment_1.online_shopping_cart.product.product_data.get_products', return_value=mock_global_products())
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=['0', 'l', 'y'])
    mocker.patch('builtins.exit', side_effect=SystemExit)

    # NOTE: Global variable 'global_products' is set at module import of this test file.
    #       The import below is to update this variable to the patch set within this test.
    from assignment_1.online_shopping_cart.checkout import checkout_process
    checkout_process.global_cart = ShoppingCart()
    with pytest.raises(SystemExit):
        checkout_process.checkout_and_payment(login_info)

    assert capsys.readouterr().out == 'Invalid input. Please try again.\nYou have been logged out.\n'


# Test 5: Add a product to the shopping cart, check out and see if its inventory is reduced
def test_checkout_reduce_product(mocker, capsys, temp_json):
    login_info = {'username': 'Maximus', 'wallet': 1000.0}
    mocker.patch('assignment_1.online_shopping_cart.product.product_data.get_products', return_value=mock_global_products())
    mocker.patch("assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME", temp_json)
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=['4', 'c', 'y', 'l', 'y'])
    mocker.patch('builtins.exit', side_effect=SystemExit)

    # NOTE: Global variable 'global_products' is set at module import of this test file.
    #       The import below is to update this variable to the patch set within this test.
    from assignment_1.online_shopping_cart.checkout import checkout_process
    checkout_process.global_cart = ShoppingCart()
    with pytest.raises(SystemExit):
        checkout_process.checkout_and_payment(login_info)

    assert checkout_process.global_products[3].units == 0


def test_checkout_and_payment6():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment7():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment8():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment9():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment10():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment11():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment12():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment13():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment14():
    # NOTE: Rename function to something appropriate
    pass


def test_checkout_and_payment15():
    # NOTE: Rename function to something appropriate
    pass