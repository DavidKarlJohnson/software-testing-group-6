###############################
# USER AUTHENTICATION CLASSES #
###############################

#from rich.console import Console

from ..user.user_data import UserDataManager
from ..user.user import CreditCard


class PasswordValidator:
    @staticmethod
    def __has_capital_letter(string: str) -> bool:
        for char in string:
            if char.isupper():
                return True
        return False

    @staticmethod
    def __has_special_symbol(string: str) -> bool:
        for char in string:
            if (not char.isdigit() and
                    not char.isalpha() and
                    not char == ' '):
                return True
        return False

    @staticmethod
    def __is_minimum_length(string: str, min_len: int) -> bool:
        if len(string) >= min_len:
            return True
        return False

    @staticmethod
    def is_valid(password) -> bool:
        # TODO: Task 1: validate password for registration
        if (PasswordValidator.__has_capital_letter(password) and
            PasswordValidator.__has_special_symbol(password) and
            PasswordValidator.__is_minimum_length(password, 8)):
                return True
        return False


class UserAuthenticator:

    @staticmethod
    def login(username, password, data) -> dict[str, str | float] | None:
        is_user_registered: bool = False

        for entry in data:
            if entry['username'].lower() == username.lower():
                is_user_registered = True
            if is_user_registered:
                if entry['password'].lower() == password.lower():
                    print('Successfully logged in.')
                    # Load credit cards if they exist
                    credit_cards = []
                    if 'credit_cards' in entry and entry['credit_cards']:
                        credit_cards = [CreditCard.from_dict(card_data) for card_data in entry['credit_cards']]
                    return {
                        'username': entry['username'],
                        'wallet': entry['wallet'],
                        'credit_cards': credit_cards
                    }
                break

        if not is_user_registered:
            print('User is not registered.')
        else:
            print('Login failed.')
        return None

    @staticmethod
    def register(username, password, data, credit_cards=None) -> None:
        new_user = {
            'username': username, 
            'password': password, 
            'wallet': 0.0,
            'credit_cards': credit_cards if credit_cards else []
        }
        data.append(new_user)
        UserDataManager.save_users(data)
