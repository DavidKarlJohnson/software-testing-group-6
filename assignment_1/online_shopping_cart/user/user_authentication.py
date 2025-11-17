###############################
# USER AUTHENTICATION CLASSES #
###############################

from rich.console import Console

from assignment_1.online_shopping_cart.user.user_data import UserDataManager


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
                    return {
                        'username': entry['username'],
                        'wallet': entry['wallet']
                    }
                break

        if not is_user_registered:
            print('User is not registered.')
        else:
            print('Login failed.')
        return None

    @staticmethod
    def register(username, password, data) -> None:
        # TODO: Task 1: register username and password as new user to file with 0.0 wallet funds
        data.append({'username': username, 'password': password, 'wallet': 0.0})
        UserDataManager.save_users(data)
