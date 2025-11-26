import pytest
from tasks_1_and_2.online_shopping_cart.checkout.checkout_process import checkout, check_cart
from tasks_1_and_2.online_shopping_cart.checkout.shopping_cart import ShoppingCart
from tasks_1_and_2.online_shopping_cart.product.product import Product
from tasks_1_and_2.online_shopping_cart.user.user import User

# ----- TASK 3.3 -----
# TODO: Write 10 test cases for the function 'checkout' located in  /online_shopping_cart/checkout/checkout_process.py


def test_checkout_empty_cart(capsys):
    user = User(name="Alice", wallet=100.0)
    cart = ShoppingCart()
    checkout(user, cart)
    captured = capsys.readouterr()
    assert captured.out == 'Your basket is empty. Please add items before checking out.\n'
    assert user.wallet == 100.0
    assert cart.is_empty()


def test_checkout_insufficient_funds(capsys):
    user = User(name="Bob", wallet=50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=60.0, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert captured.out == "You don't have enough money to complete the purchase. Please try again!\n"
    assert user.wallet == 50.0
    assert not cart.is_empty()


def test_checkout_success_single_item(capsys):
    user = User(name="Carol", wallet=10.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Banana", price=2.0, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert 'Thank you for your purchase, Carol! Your remaining balance is 8.0\n' == captured.out
    assert user.wallet == 8.0
    assert cart.is_empty()


def test_checkout_exact_wallet_zero(capsys):
    user = User(name="Dave", wallet=5.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Bread", price=2.5, units=1))
    cart.add_item(Product(name="Bread", price=2.5, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert 'Thank you for your purchase, Dave! Your remaining balance is 0.0\n' == captured.out
    assert user.wallet == 0.0
    assert cart.is_empty()


def test_checkout_multiple_units_total(capsys):
    user = User(name="Eve", wallet=100.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Milk", price=3.0, units=1))
    cart.add_item(Product(name="Milk", price=3.0, units=1))
    cart.add_item(Product(name="Milk", price=3.0, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert 'Thank you for your purchase, Eve! Your remaining balance is 91.0\n' == captured.out
    assert user.wallet == 91.0
    assert cart.is_empty()


def test_checkout_multiple_products(capsys):
    user = User(name="Frank", wallet=50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Eggs", price=5.0, units=1))
    cart.add_item(Product(name="Cheese", price=7.5, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert 'Thank you for your purchase, Frank! Your remaining balance is 37.5\n' == captured.out
    assert user.wallet == 37.5
    assert cart.is_empty()


def test_checkout_does_not_clear_on_insufficient_funds(capsys):
    user = User(name="Gina", wallet=5.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Chocolate", price=10.0, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert captured.out == "You don't have enough money to complete the purchase. Please try again!\n"
    assert not cart.is_empty()
    assert user.wallet == 5.0


def test_checkout_total_price_with_units(capsys):
    user = User(name="Henry", wallet=20.0)
    cart = ShoppingCart()
    p = Product(name="Juice", price=4.0, units=1)
    cart.add_item(p)
    cart.add_item(p)
    checkout(user, cart)
    captured = capsys.readouterr()
    assert 'Thank you for your purchase, Henry! Your remaining balance is 12.0\n' == captured.out
    assert user.wallet == 12.0
    assert cart.is_empty()


def test_checkout_wallet_float_precision(capsys):
    user = User(name="Ivy", wallet=10.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Snack", price=3.3333333, units=1))
    cart.add_item(Product(name="Snack", price=3.3333333, units=1))
    cart.add_item(Product(name="Snack", price=3.3333334, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert user.wallet == pytest.approx(0.0, abs=1e-6)
    assert cart.is_empty()
    assert captured.out.startswith('Thank you for your purchase, Ivy!')


def test_checkout_prints_username_and_balance(capsys):
    user = User(name="Jack", wallet=15.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Water", price=5.0, units=1))
    checkout(user, cart)
    captured = capsys.readouterr()
    assert captured.out == 'Thank you for your purchase, Jack! Your remaining balance is 10.0\n'
    assert user.wallet == 10.0
    assert cart.is_empty()



# ----- TASK 3.3 -----
# TODO: Write 10 test cases for the function 'check_cart' located in  /online_shopping_cart/checkout/checkout_process.py


def test_check_cart_empty_returns_false(capsys):
    user = User(name="Alice", wallet=100.0)
    cart = ShoppingCart()
    result = check_cart(user, cart)
    captured = capsys.readouterr()
    assert result is False
    assert 'Items in the cart:\n' in captured.out


def test_check_cart_checkout_yes(mocker, capsys):
    user = User(name="Bob", wallet=10.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=2.0, units=1))
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['y'])
    result = check_cart(user, cart)
    captured = capsys.readouterr()
    assert result is None
    assert cart.is_empty()
    assert user.wallet == 8.0
    assert 'Thank you for your purchase, Bob! Your remaining balance is 8.0\n' in captured.out


def test_check_cart_checkout_no_remove_no_returns_false(mocker):
    user = User(name="Carol", wallet=10.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Banana", price=1.0, units=1))
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['n', 'n'])
    result = check_cart(user, cart)
    assert result is False
    assert not cart.is_empty()


def test_check_cart_remove_display_then_exit(mocker):
    user = User(name="Dave", wallet=20.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Bread", price=2.5, units=1))
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['n', 'y', 'c', 'n', 'n'])
    result = check_cart(user, cart)
    assert result is False
    assert not cart.is_empty()


def test_check_cart_remove_valid_index_updates_cart_and_inventory(mocker):
    from assignment_1.online_shopping_cart.checkout import checkout_process
    user = User(name="Eve", wallet=50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Milk", price=3.0, units=1))
    cart.add_item(Product(name="Milk", price=3.0, units=1))
    checkout_process.global_products = [Product(name="Milk", price=3.0, units=10)]
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['n', 'y', '1', 'n', 'n'])
    result = check_cart(user, cart)
    assert result is False
    assert cart.retrieve_items()[0].units == 1
    assert checkout_process.global_products[0].units == 11


def test_check_cart_remove_invalid_index_prints_error(mocker, capsys):
    user = User(name="Frank", wallet=50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Eggs", price=5.0, units=1))
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['n', 'y', '99', 'n', 'n'])
    check_cart(user, cart)
    captured = capsys.readouterr()
    assert 'Invalid input. Please try again.\n' in captured.out
    assert not cart.is_empty()


def test_check_cart_remove_non_digit_prints_error(mocker, capsys):
    user = User(name="Gina", wallet=50.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Cheese", price=7.5, units=1))
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['n', 'y', 'abc', 'n', 'n'])
    check_cart(user, cart)
    captured = capsys.readouterr()
    assert 'Invalid input. Please try again.\n' in captured.out
    assert not cart.is_empty()


def test_check_cart_remove_until_empty(mocker):
    user = User(name="Henry", wallet=50.0)
    cart = ShoppingCart()
    p = Product(name="Juice", price=4.0, units=1)
    cart.add_item(p)
    cart.add_item(p)
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['n', 'y', '1', 'n', 'y', '1', 'n', 'n'])
    result = check_cart(user, cart)
    assert result is False
    assert cart.is_empty()


def test_check_cart_checkout_uppercase_yes(mocker):
    user = User(name="Ivy", wallet=10.0)
    cart = ShoppingCart()
    cart.add_item(Product(name="Snack", price=3.0, units=1))
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['Y'])
    result = check_cart(user, cart)
    assert result is None
    assert cart.is_empty()
    assert user.wallet == 7.0


def test_check_cart_empty_even_if_user_inputs(mocker):
    user = User(name="Jack", wallet=10.0)
    cart = ShoppingCart()
    mocker.patch("assignment_1.online_shopping_cart.user.user_interface.UserInterface.get_user_input", side_effect=['y'])
    result = check_cart(user, cart)
    assert result is False
    assert cart.is_empty()
