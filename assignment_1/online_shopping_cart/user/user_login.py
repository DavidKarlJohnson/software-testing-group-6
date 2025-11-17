from assignment_1.online_shopping_cart.user.user_authentication import UserAuthenticator, PasswordValidator
from assignment_1.online_shopping_cart.user.user_interface import UserInterface
from assignment_1.online_shopping_cart.user.user_data import UserDataManager


########################
# USER LOGIN FUNCTIONS #
########################

def is_quit(input_argument: str) -> bool:
    return input_argument.lower() == 'q'



def login() -> dict[str, str | float] | None:
    username: str = UserInterface.get_user_input(prompt="Enter your username (or 'q' to quit): ")
    if is_quit(input_argument=username):
        exit(0)  # The user has quit

    password: str = UserInterface.get_user_input(prompt="Enter your password (or 'q' to quit): ")
    if is_quit(input_argument=password):
        exit(0)   # The user has quit

    is_authentic_user: dict[str, str | float] = UserAuthenticator().login(
        username=username,
        password=password,
        data=UserDataManager.load_users()
    )

    if is_authentic_user is not None:
        return is_authentic_user

    # TODO: Task 1: prompt user to register when not found
    register_new_user: str = UserInterface.get_user_input(prompt=f"Would you like to register new user  '{username}': y/n ? ")
    if register_new_user.lower() != 'y':
        return None

    new_password: str = UserInterface.get_user_input(prompt="Password: ")

    if PasswordValidator.is_valid(new_password):
        UserAuthenticator.register(username=username, password=new_password, data=UserDataManager.load_users())
        print('Saved new user')
    else:
        print('Invalid password, please give a password with a minimum length of 8 characters, at lease one capital letter and one special symbol')
    return None
