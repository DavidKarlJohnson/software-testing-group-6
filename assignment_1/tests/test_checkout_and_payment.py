import json
import os
import tempfile
from copy import deepcopy

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


# Helper function for setting up the testing environment for 'checkout_and_payment'.
# Function will: (1) Patch 'products.csv' and 'users.json' files,
#                (2) Re-import 'checkout_process' module to refresh global variables
#                (3) Create global ShoppingCart object
#                (4) Call 'checkout_and_payment' with a pre-defined user
def setup_reimport_initialize(mocker, temp_products=None, temp_json=None):
    login_info = {'username': 'Maximus', 'wallet': 1000.0}
    mocker.patch('builtins.exit', side_effect=SystemExit)
    if temp_products is not None:
        mocker.patch('assignment_1.online_shopping_cart.product.product_data.get_products', return_value=deepcopy(temp_products))
    if temp_json is not None:
        mocker.patch("assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME", temp_json)

    # NOTE: Global variable 'global_products' is set at module import of this test file.
    #       The import below is to update this variable to the patch set within this test.
    from assignment_1.online_shopping_cart.checkout import checkout_process
    checkout_process.global_products = deepcopy(temp_products)
    checkout_process.global_cart = ShoppingCart()

    with pytest.raises(SystemExit):
        checkout_process.checkout_and_payment(login_info)

    return checkout_process


@pytest.mark.parametrize(
    ('user_input', 'expected_output'),
     [
        # Test 1: Add the first product (1) within the acceptable bounds [1,5]
         (['1', 'l', 'y'],
          'Apple added to your cart.\n'
          'Your cart is not empty. You have the following items:\n'
          'Apple - $2.0 - Units: 1\n''You have been logged out.\n'),
        # Test 2: Add the last product (5) within the acceptable bounds [1,5]
         (['5', 'l', 'y'],
          'Strawberry added to your cart.\n'
          'Your cart is not empty. You have the following items:\n'
          'Strawberry - $4.0 - Units: 1\n''You have been logged out.\n'),
        # Test 3: Add a product (6) that's out of bounds [1,5]
         (['6', 'l', 'y'],
          'Invalid input. Please try again.\n'
          'You have been logged out.\n'),
        # Test 4: Add a product (0) that's out of bounds [1,5]
         (['0', 'l', 'y'],
          'Invalid input. Please try again.\n'
          'You have been logged out.\n'),
     ],
     ids=['Products is within bounds, lower',
          'Products is within bounds, upper',
          'Products is out of bounds, upper',
          'Products is out of bounds, lower',]
)
def test_add_product_boundaries(user_input, expected_output, mocker, capsys):
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=user_input)
    setup_reimport_initialize(mocker, mock_global_products())
    assert capsys.readouterr().out == expected_output


# Test 5: Add a product to the shopping cart, checkout and see if its inventory is reduced
def test_checkout_reduce_product(mocker, temp_json):
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input", side_effect=['4', 'c', 'y', 'l', 'y'])
    setup = setup_reimport_initialize(mocker, mock_global_products(), temp_json)
    assert setup.global_products[3].units == 0


# Test 6: Print out all the available products for purchase
def test_print_stock(mocker, capsys):
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
                 side_effect=['d', 'l', 'y'])
    setup_reimport_initialize(mocker, mock_global_products())
    assert capsys.readouterr().out ==  ('\nAvailable products for purchase:\n'
                                        '1. Apple - $2.0 - Units: 10\n'
                                        '2. Banana - $1.0 - Units: 15\n'
                                        '3. Orange - $1.5 - Units: 8\n'
                                        '4. Grapes - $3.0 - Units: 1\n'
                                        '5. Strawberry - $4.0 - Units: 12\n'
                                        'You have been logged out.\n')


# Test 7: User navigates to checkout with an empty cart
def test_checkout_empty_cart(mocker, capsys):
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
                 side_effect=['c', 'l', 'y'])
    setup_reimport_initialize(mocker, mock_global_products())
    assert capsys.readouterr().out == ('\nItems in the cart:'
                                       '\nYou have been logged out.\n')


# Test 8: Add to cart a product that's not in stock
def test_add_product_no_stock(mocker, capsys):
    mocker.patch("assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
                 side_effect=['1', 'l', 'y'])
    setup_reimport_initialize(mocker, [Product(name='Kex', price=2.0, units=0),
            Product(name='Banana', price=1.0, units=15),
            Product(name='Orange', price=1.5, units=8),
            Product(name='Grapes', price=3.0, units=1),
            Product(name='Strawberry', price=4.0, units=12)])
    assert capsys.readouterr().out == ('Sorry, Kex is out of stock.'
                                      '\nYou have been logged out.\n')


# Test 9: Remove an item from the cart
def test_remove_valid_product_from_cart():
    # PSEUDO CODE:
    # USER NAVIGATION:  *Add items to cart* > "C" > Do you want to checkout? > "N" > Do you want to remove and item > "Y" > *Enters number out of bounds* > Invalid input. Please try again > Do you want to checkout Y/N?
    pass


# Test 10: Remove an item that's not in the cart (out of bounds)
def test_remove_invalid_product_from_cart():
    # PSEUDO CODE:
    # USER NAVIGATION:  *Add items to cart* > "C" > Do you want to checkout? > "N" > Do you want to remove and item > "Y" > *Enters number within bounds* > ***Check in test that items are removed from cart***
    pass


# Test 11: Checkout and see if cart is cleared
def test_checkout_clear_cart():
    # PSEUDO CODE:
    # USER NAVIGATION:  *Items already in cart* > Do you want to checkout? > "Y" > *System prints thank you* > *Check in test if item is checked out*
    pass


# Test 12: Logout with a cart that's not empty
def test_logout_non_empty_cart():
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