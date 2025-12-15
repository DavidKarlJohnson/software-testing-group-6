################
# USER CLASSES #
################


class CreditCard:
    """
    CreditCard class to represent a credit card
    """
    def __init__(self, card_number: str, expiry_date: str, name_on_card: str, cvv: str) -> None:
        self.card_number: str = card_number
        self.expiry_date: str = expiry_date
        self.name_on_card: str = name_on_card
        self.cvv: str = cvv

    def to_dict(self) -> dict:
        """Convert credit card to dictionary for JSON serialization"""
        return {
            'card_number': self.card_number,
            'expiry_date': self.expiry_date,
            'name_on_card': self.name_on_card,
            'cvv': self.cvv
        }

    @staticmethod
    def from_dict(data: dict) -> 'CreditCard':
        """Create CreditCard from dictionary"""
        return CreditCard(
            card_number=data['card_number'],
            expiry_date=data['expiry_date'],
            name_on_card=data['name_on_card'],
            cvv=data['cvv']
        )


class User:
    """
    User class to represent user information
    """

    def __init__(self, name, wallet, credit_cards=None) -> None:
        self.name: str = name
        self.wallet: float = wallet
        self.credit_cards: list[CreditCard] = credit_cards if credit_cards else []
