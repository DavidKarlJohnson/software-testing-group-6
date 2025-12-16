import pytest
import json
import os
import tempfile
from copy import deepcopy
from unittest.mock import Mock, patch, MagicMock

from tasks_1_and_2.online_shopping_cart.checkout.checkout_process import checkout, check_cart
from tasks_1_and_2.online_shopping_cart.checkout.shopping_cart import ShoppingCart
from tasks_1_and_2.online_shopping_cart.product.product import Product
from tasks_1_and_2.online_shopping_cart.user.user import User, CreditCard


@pytest.fixture
def sample_user_with_cards():
    """User with multiple credit cards"""
    user = User(name="TestUser", wallet=1000.0)
    user.credit_cards = [
        CreditCard("1234567890123456", "12/25", "Test User", "123"),
        CreditCard("5555666677778888", "09/27", "Test User", "456"),
    ]
    return user


@pytest.fixture
def sample_user_no_cards():
    """User with no credit cards"""
    return User(name="TestUser", wallet=1000.0)


@pytest.fixture
def sample_products():
    """Sample products for testing"""
    return [
        Product(name='Apple', price=2.0, units=10),
        Product(name='Banana', price=1.0, units=15),
        Product(name='Orange', price=1.5, units=8),
    ]


@pytest.fixture
def empty_cart():
    """Empty shopping cart"""
    return ShoppingCart()


@pytest.fixture
def cart_with_items():
    """Cart with items"""
    cart = ShoppingCart()
    cart.add_item(Product(name='Apple', price=2.0, units=1))
    cart.add_item(Product(name='Banana', price=1.0, units=2))
    return cart



def test_prime_path_1_empty_cart_checkout(sample_user_no_cards, empty_cart, capsys):
    """
    Prime Path 1: Empty cart condition check
    Tests the early exit when cart is empty.
    Sidetrips: None, Detours: None
    """
    checkout(sample_user_no_cards, empty_cart)
    captured = capsys.readouterr()
    assert 'Your basket is empty' in captured.out



def test_prime_path_2_wallet_payment_sufficient_funds(sample_user_with_cards, cart_with_items, capsys):
    """
    Prime Path 2: Wallet payment with sufficient funds
    Total price: Apple (2.0) + Banana (2.0) = 4.0
    User wallet: 1000.0
    Sidetrips: None, Detours: None
    """
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.return_value = 'wallet'
        
        initial_wallet = sample_user_with_cards.wallet
        checkout(sample_user_with_cards, cart_with_items)
        
        assert sample_user_with_cards.wallet == initial_wallet - 4.0
        assert cart_with_items.is_empty()
        captured = capsys.readouterr()
        assert 'Thank you for your purchase' in captured.out



def test_prime_path_3_wallet_payment_insufficient_funds(empty_cart, capsys):
    """
    Prime Path 3: Wallet payment with insufficient funds
    User has 5.0 wallet, cart total is 10.0
    Sidetrips: None, Detours: None
    """
    user = User(name="PoorUser", wallet=5.0)
    cart = ShoppingCart()
    cart.add_item(Product(name='Expensive', price=10.0, units=1))
    
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.return_value = 'wallet'
        
        checkout(user, cart)
        
        assert user.wallet == 5.0  # Wallet unchanged
        assert not cart.is_empty()  # Cart still has items
        captured = capsys.readouterr()
        assert "don't have enough money" in captured.out



def test_prime_path_4_card_payment_no_cards_registered(sample_user_no_cards, cart_with_items, capsys):
    """
    Prime Path 4: Card payment with no cards registered
    User selects 'card' but has no cards, falls back to wallet
    Sidetrips: None, Detours: Yes (fallback to wallet)
    """
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.return_value = 'card'
        
        initial_wallet = sample_user_no_cards.wallet
        checkout(sample_user_no_cards, cart_with_items)
        
        captured = capsys.readouterr()
        assert 'no credit cards registered' in captured.out
        # Should fall back to wallet payment
        assert sample_user_no_cards.wallet == initial_wallet - 4.0



def test_prime_path_5_card_payment_valid_selection(sample_user_with_cards, cart_with_items, capsys):
    """
    Prime Path 5: Card payment with valid card selection
    User selects card #1 from available cards
    Sidetrips: None, Detours: None
    """
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.side_effect = ['card', '1']
        
        checkout(sample_user_with_cards, cart_with_items)
        
        assert cart_with_items.is_empty()
        captured = capsys.readouterr()
        assert 'Paying' in captured.out
        assert '3456' in captured.out  # Last 4 digits of first card



def test_prime_path_6_card_payment_invalid_index_high(sample_user_with_cards, cart_with_items, capsys):
    """
    Prime Path 6: Card payment with invalid card index (too high)
    User has 2 cards but selects card #5
    Sidetrips: None, Detours: None
    """
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.side_effect = ['card', '5']
        
        checkout(sample_user_with_cards, cart_with_items)
        
        assert not cart_with_items.is_empty()  # Cart unchanged
        captured = capsys.readouterr()
        assert 'Invalid card selection' in captured.out



def test_prime_path_7_card_payment_non_numeric_input(sample_user_with_cards, cart_with_items, capsys):
    """
    Prime Path 7: Card payment with non-numeric card selection
    User enters 'abc' instead of a number
    Sidetrips: None, Detours: None
    """
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.side_effect = ['card', 'abc']
        
        checkout(sample_user_with_cards, cart_with_items)
        
        assert not cart_with_items.is_empty()
        captured = capsys.readouterr()
        assert 'Invalid card selection' in captured.out



def test_prime_path_8_check_cart_empty_cart(sample_user_with_cards, capsys):
    """
    Prime Path 8: check_cart with empty cart
    User is shown empty cart and cannot proceed
    Sidetrips: None, Detours: None
    """
    cart = ShoppingCart()
    
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.return_value = 'no'
        
        result = check_cart(sample_user_with_cards, cart)
        
        assert result is False
        captured = capsys.readouterr()
        assert 'Items in the cart' in captured.out



def test_prime_path_9_check_cart_immediate_checkout(sample_user_with_cards, cart_with_items, capsys):
    """
    Prime Path 9: check_cart with immediate checkout
    User displays cart and immediately chooses to checkout
    Sidetrips: Yes (calls checkout), Detours: No
    """
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        # First call: checkout decision
        mock_input.side_effect = ['yes', 'wallet']
        
        check_cart(sample_user_with_cards, cart_with_items)
        
        assert cart_with_items.is_empty()
        captured = capsys.readouterr()
        assert 'Thank you for your purchase' in captured.out



def test_prime_path_10_check_cart_remove_item(sample_user_with_cards, capsys):
    """
    Prime Path 10: check_cart with item removal
    User removes an item from cart, then exits loop
    Sidetrips: Yes (remove_item call), Detours: Yes (while loop)
    """
    cart = ShoppingCart()
    cart.add_item(Product(name='Apple', price=2.0, units=2))
    
    with patch('tasks_1_and_2.online_shopping_cart.user.user_interface.UserInterface.get_user_input') as mock_input:
        mock_input.side_effect = ['no', 'yes', '1', 'no', 'no']
        
        result = check_cart(sample_user_with_cards, cart)
        
        # Item should be removed (units decreased from 2 to 1, so still in cart)
        assert len(cart.retrieve_items()) == 1
        assert cart.retrieve_items()[0].units == 1
        assert result is False
        captured = capsys.readouterr()
        assert 'Items in the cart' in captured.out