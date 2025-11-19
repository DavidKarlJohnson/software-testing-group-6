import pytest
import os

from assignment_1.online_shopping_cart.checkout.shopping_cart import ShoppingCart
from assignment_1.online_shopping_cart.product.product import Product
from assignment_1.online_shopping_cart.user.user_logout import logout



# ----- TASK 3.1 -----
# TODO: Write 10 test cases for the function 'logout' located in  /online_shopping_cart/user/user_logout.py


# Test #1: Test different variants of 'yes' for confirming logout
@pytest.mark.parametrize('user_input, expected',
                         [('y', True),
                          ('yes', True),
                          ('yeah', True),
                          ('yyyyyy', True),
                          ('no', False)])
def test_logout_confirmation_yes(mocker, user_input, expected):
    shopping_cart = ShoppingCart()
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_logout.UserInterface.get_user_input",
        side_effect=[user_input])

    result = logout(shopping_cart)
    assert result == expected


# Test #2: Test different variants of 'no' for canceling logout
@pytest.mark.parametrize('user_input, expected',
                         [('n', False),
                          ('no', False),
                          ('abc', False),
                          ('!', False),
                          (' ', False),
                          ('y', True)])
def test_logout_confirmation_no(mocker, user_input, expected):
    shopping_cart = ShoppingCart()
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_logout.UserInterface.get_user_input",
        side_effect=[user_input])

    result = logout(shopping_cart)
    assert result == expected


# Test #3: Test capitalization of confirmation to logout
@pytest.mark.parametrize('user_input, expected',
                         [('Y', True),
                          ('Yes', True),
                          ('N', False),
                          ('No', False)])
def test_logout_confirmation_capitalization(mocker, user_input, expected):
    shopping_cart = ShoppingCart()
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_logout.UserInterface.get_user_input",
        side_effect=[user_input])

    result = logout(shopping_cart)
    assert result == expected


# Test #4: Non-empty cart warning when logging out
def test_logout_with_non_empty_cart(mocker, capsys):
    shopping_cart = ShoppingCart()
    shopping_cart.add_item(Product(name='Carrot', price=10.0, units=1))
    shopping_cart.add_item(Product(name='Egg', price=20.0, units=2))
    shopping_cart.add_item(Product(name='Shoe', price=30.0, units=2))

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_logout.UserInterface.get_user_input",
        side_effect='n')

    logout(shopping_cart)
    captured_output = capsys.readouterr().out
    assert captured_output == 'Your cart is not empty. You have the following items:\n''Carrot - $10.0 - Units: 1\n''Egg - $20.0 - Units: 2\n''Shoe - $30.0 - Units: 2\n'


def test_logout5():
    # NOTE: Rename function to something appropriate
    pass


def test_logout6():
    # NOTE: Rename function to something appropriate
    pass


def test_logout7():
    # NOTE: Rename function to something appropriate
    pass


def test_logout8():
    # NOTE: Rename function to something appropriate
    pass


def test_logout9():
    # NOTE: Rename function to something appropriate
    pass


def test_logout10():
    # NOTE: Rename function to something appropriate
    pass


