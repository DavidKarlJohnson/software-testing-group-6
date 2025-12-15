import pytest
from tasks_1_and_2.online_shopping_cart.user.user import User, CreditCard
from tasks_1_and_2.online_shopping_cart.user.credit_card_manager import CreditCardManager


# Test 1: Add a credit card to user profile
def test_add_credit_card():
    user = User(name="TestUser", wallet=100.0)
    assert len(user.credit_cards) == 0
    
    CreditCardManager.add_credit_card(
        user=user,
        card_number="1234567890123456",
        expiry_date="12/25",
        name_on_card="Test User",
        cvv="123"
    )
    
    assert len(user.credit_cards) == 1
    assert user.credit_cards[0].card_number == "1234567890123456"
    assert user.credit_cards[0].expiry_date == "12/25"
    assert user.credit_cards[0].name_on_card == "Test User"
    assert user.credit_cards[0].cvv == "123"


# Test 2: Remove a credit card from user profile
def test_remove_credit_card():
    user = User(name="TestUser", wallet=100.0)
    CreditCardManager.add_credit_card(user, "1111222233334444", "06/26", "John Doe", "456")
    CreditCardManager.add_credit_card(user, "5555666677778888", "09/27", "John Doe", "789")
    
    assert len(user.credit_cards) == 2
    
    # Remove first card
    result = CreditCardManager.remove_credit_card(user, 0)
    assert result is True
    assert len(user.credit_cards) == 1
    assert user.credit_cards[0].card_number == "5555666677778888"


# Test 3: Update credit card details
def test_update_credit_card():
    user = User(name="TestUser", wallet=100.0)
    CreditCardManager.add_credit_card(user, "9999888877776666", "03/25", "Jane Smith", "321")
    
    # Update expiry date and CVV
    result = CreditCardManager.update_credit_card(
        user=user,
        card_index=0,
        expiry_date="12/28",
        cvv="999"
    )
    
    assert result is True
    assert user.credit_cards[0].card_number == "9999888877776666"  # unchanged
    assert user.credit_cards[0].expiry_date == "12/28"  # updated
    assert user.credit_cards[0].name_on_card == "Jane Smith"  # unchanged
    assert user.credit_cards[0].cvv == "999"  # updated
