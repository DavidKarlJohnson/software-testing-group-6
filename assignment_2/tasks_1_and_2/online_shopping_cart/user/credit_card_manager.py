from ..user.user import CreditCard, User
from ..user.user_data import UserDataManager


class CreditCardManager:
    """
    Manages credit card operations for users
    """

    @staticmethod
    def add_credit_card(user: User, card_number: str, expiry_date: str, name_on_card: str, cvv: str) -> None:
        """Add a new credit card to the user's profile"""
        new_card = CreditCard(card_number, expiry_date, name_on_card, cvv)
        user.credit_cards.append(new_card)

    @staticmethod
    def remove_credit_card(user: User, card_index: int) -> bool:
        """Remove a credit card by index. Returns True if successful."""
        if 0 <= card_index < len(user.credit_cards):
            user.credit_cards.pop(card_index)
            return True
        return False

    @staticmethod
    def update_credit_card(user: User, card_index: int, card_number: str = None, 
                          expiry_date: str = None, name_on_card: str = None, cvv: str = None) -> bool:
        """Update credit card details. Returns True if successful."""
        if 0 <= card_index < len(user.credit_cards):
            card = user.credit_cards[card_index]
            if card_number:
                card.card_number = card_number
            if expiry_date:
                card.expiry_date = expiry_date
            if name_on_card:
                card.name_on_card = name_on_card
            if cvv:
                card.cvv = cvv
            return True
        return False

    @staticmethod
    def save_user_cards(username: str, user: User) -> None:
        """Save user's credit cards to the user data file"""
        data = UserDataManager.load_users()
        for entry in data:
            if entry['username'] == username:
                entry['credit_cards'] = [card.to_dict() for card in user.credit_cards]
                break
        UserDataManager.save_users(data)
