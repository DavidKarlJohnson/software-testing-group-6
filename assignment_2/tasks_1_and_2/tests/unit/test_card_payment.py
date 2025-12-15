import pytest
from tasks_1_and_2.online_shopping_cart.checkout.checkout_process import checkout
from tasks_1_and_2.online_shopping_cart.checkout.shopping_cart import ShoppingCart
from tasks_1_and_2.online_shopping_cart.product.product import Product
from tasks_1_and_2.online_shopping_cart.user.user import User, CreditCard


# Test 1: Successful payment with credit card
def test_checkout_with_valid_card(mocker, capsys):
    user = User(name="Alice", wallet=10.0)
    card = CreditCard(
        card_number="1234567890123456",
        expiry_date="12/25",
        name_on_card="Alice Smith",
        cvv="123"
    )
    user.credit_cards.append(card)
    
    cart = ShoppingCart()
    cart.add_item(Product(name="Apple", price=50.0, units=1))
    
    # Mock user selecting card payment and card #1
    mocker.patch(
        "tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input",
        side_effect=['card', '1']
    )
    
    checkout(user, cart)
    captured = capsys.readouterr()
    
    assert 'Paying $50.00 with card ending in 3456' in captured.out
    assert 'Thank you for your purchase, Alice!' in captured.out
    assert cart.is_empty()
    assert user.wallet == 10.0  # Wallet unchanged when paying with card


# Test 2: Checkout with no credit cards falls back to wallet
def test_checkout_no_cards_uses_wallet(mocker, capsys):
    user = User(name="Bob", wallet=100.0)
    # No credit cards
    
    cart = ShoppingCart()
    cart.add_item(Product(name="Banana", price=20.0, units=1))
    
    # User tries to pay with card but has none
    mocker.patch(
        "tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input",
        return_value='card'
    )
    
    checkout(user, cart)
    captured = capsys.readouterr()
    
    assert 'You have no credit cards registered. Using wallet instead.' in captured.out
    assert 'Thank you for your purchase, Bob! Your remaining balance is 80.0' in captured.out
    assert cart.is_empty()
    assert user.wallet == 80.0


# Test 3: Invalid card selection cancels payment
def test_checkout_invalid_card_selection(mocker, capsys):
    user = User(name="Carol", wallet=50.0)
    card = CreditCard("9876543210987654", "06/26", "Carol Jones", "456")
    user.credit_cards.append(card)
    
    cart = ShoppingCart()
    cart.add_item(Product(name="Orange", price=15.0, units=1))
    
    # User selects card payment but provides invalid card number
    mocker.patch(
        "tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input",
        side_effect=['card', '99']  # Invalid card index
    )
    
    checkout(user, cart)
    captured = capsys.readouterr()
    
    assert 'Invalid card selection. Payment cancelled.' in captured.out
    assert not cart.is_empty()  # Cart should not be cleared
    assert user.wallet == 50.0  # Wallet unchanged
