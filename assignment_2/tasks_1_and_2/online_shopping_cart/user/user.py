################
# USER CLASSES #
################


# TODO - TASK 1: Implementation 1: Strengthening the user profile. (3 points)
# Expand the user file with credit card details for an arbitrary number of credit
# cards. Each card has a card number, date of expiry, name on card, CVV for
# each card. Add a module that allows the user to change these details in the file.
# Expand the user registration to allow entry of these additional details.

class User:
    """
    User class to represent user information
    """

    def __init__(self, name, wallet) -> None:
        self.name: str = name
        self.wallet: float = wallet
