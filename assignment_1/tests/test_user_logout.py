import pytest

from assignment_1.online_shopping_cart.checkout.shopping_cart import ShoppingCart
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
    cart: ShoppingCart = ShoppingCart()
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_logout.UserInterface.get_user_input",
        side_effect=[user_input])

    result = logout(cart)
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
    cart: ShoppingCart = ShoppingCart()
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_logout.UserInterface.get_user_input",
        side_effect=[user_input])

    result = logout(cart)
    assert result == expected
    pass


def test_logout3():
    # NOTE: Rename function to something appropriate
    pass


def test_logout4():
    # NOTE: Rename function to something appropriate
    pass


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


