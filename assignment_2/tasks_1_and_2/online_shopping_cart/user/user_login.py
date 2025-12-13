from ..user.user_authentication import UserAuthenticator, PasswordValidator
from ..user.user_interface import UserInterface
from ..user.user_data import UserDataManager
from ..user.credit_card_manager import CreditCardManager


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
        # Show menu for managing profile
        while True:
            choice = UserInterface.get_user_input(
                prompt="\n1. Continue shopping\n2. Manage credit cards\nChoose option: "
            )
            
            if choice == '1':
                # Reload user data to get any changes made in credit card management
                users = UserDataManager.load_users()
                for user_entry in users:
                    if user_entry['username'] == username:
                        return user_entry
                return is_authentic_user
            elif choice == '2':
                manage_credit_cards(username)
            else:
                print("Invalid option, try again")
                continue


    # TODO - TASK 1: Implementation 1: Strengthening the user profile. (3 points)
    # Expand the user file with credit card details for an arbitrary number of credit
    # cards. Each card has a card number, date of expiry, name on card, CVV for
    # each card. Add a module that allows the user to change these details in the file.
    # Expand the user registration to allow entry of these additional details.
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


def manage_credit_cards(username: str) -> None:
    """Manage credit cards for logged in user"""
    from ..user.user import User, CreditCard
    
    users = UserDataManager.load_users()
    user_data = None
    for user_entry in users:
        if user_entry['username'] == username:
            user_data = user_entry
            break
    
    if not user_data:
        print("User not found")
        return
    
    user = User(
        name=username,
        wallet=user_data['wallet'],
        credit_cards=[CreditCard.from_dict(c) for c in user_data.get('credit_cards', [])]
    )
    
    while True:
        print(f"\n--- Credit Cards for {username} ---")
        if user.credit_cards:
            for i, card in enumerate(user.credit_cards, 1):
                print(f"{i}. {card.name_on_card} - **** {card.card_number[-4:]} (Exp: {card.expiry_date})")
        else:
            print("No credit cards on file")
        
        print("\n1. Add card\n2. Remove card\n3. Update card\n4. Back to menu")
        choice = UserInterface.get_user_input(prompt="Choose option: ")
        
        if choice == '1':
            card_number = UserInterface.get_user_input(prompt="Card number: ")
            expiry = UserInterface.get_user_input(prompt="Expiry date (MM/YY): ")
            name = UserInterface.get_user_input(prompt="Name on card: ")
            cvv = UserInterface.get_user_input(prompt="CVV: ")
            CreditCardManager.add_credit_card(user, card_number, expiry, name, cvv)
            CreditCardManager.save_user_cards(username, user)
            print("Card added!")
            
        elif choice == '2':
            if not user.credit_cards:
                print("No cards to remove")
                continue
            card_idx = UserInterface.get_user_input(prompt="Enter card number to remove: ")
            try:
                if CreditCardManager.remove_credit_card(user, int(card_idx) - 1):
                    CreditCardManager.save_user_cards(username, user)
                    print("Card removed!")
                else:
                    print("Invalid card number")
            except ValueError:
                print("Invalid card number")
                
        elif choice == '3':
            if not user.credit_cards:
                print("No cards to update")
                continue
            card_idx = UserInterface.get_user_input(prompt="Enter card number to update: ")
            try:
                idx = int(card_idx) - 1
                print("Leave blank to keep current value")
                name = UserInterface.get_user_input(prompt=f"Name on card [{user.credit_cards[idx].name_on_card}]: ")
                cvv = UserInterface.get_user_input(prompt=f"CVV: ")
                
                if CreditCardManager.update_credit_card(user, idx, name_on_card=name or None, cvv=cvv or None):
                    CreditCardManager.save_user_cards(username, user)
                    print("Card updated!")
                else:
                    print("Invalid card number")
            except (ValueError, IndexError):
                print("Invalid card number")
                
        elif choice == '4':
            break
        else:
            print("Invalid option")
