import tempfile
import pytest
import json
import os
from pytest_mock import mocker
from assignment_1.online_shopping_cart.user.user_login import login



# ----- TASK 3.1 -----
# TODO: Write 10 test cases for the function 'login' located in  /online_shopping_cart/user/user_login.py


# Fixture for temporary JSON file to be used in tests
@pytest.fixture
def temp_json():
    data = [{"username": "Ramanathan",
            "password": "Notaproblem23*",
            "wallet": 100.0
            },
             {
            "username": "Samantha",
            "password": "SecurePass123/^",
            "wallet": 150.0
             },
             {
            "username": "Maximus",
            "password": "StrongPwd!23",
            "wallet": 75.0
    }]
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_json:
        json.dump(data, tmp_json)
        tmp_json.flush()
        yield tmp_json.name

    os.remove(tmp_json.name)


# Helper function for reading JSON files
def json_to_list(file):
    with open(file, 'r') as f:
        return json.load(f)


# Test 1: Log in an existing user
def test_successful_login(mocker, temp_json):
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=['Maximus', 'StrongPwd!23'])

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    result = login()
    assert result is not None


# Test 2: Register a new user with valid password and see if it's stored in the JSON file.
def test_register_save_new_user(mocker, capsys, temp_json):
    username = 'Jimmy'
    password = 'Password123!'

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=[username, 'password123', 'y', password])

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    login()
    assert json_to_list(temp_json)[-1] == {'username': username, 'password': password, 'wallet': 0.0}


# Test 3: The user declines the prompt to register a new user
def test_decline_register_new_user(mocker, temp_json):
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=['Monkey', 'password123', 'n'])


    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    result = login()
    assert result is None


# Test 4: Register new user with invalid password - no special character
def test_register_user_invalid_pw_no_special_char(mocker, temp_json, capsys):
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=['Jake', 'password123', 'y', 'Password123'])

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    login()
    captured_output = capsys.readouterr().out
    assert captured_output == 'User is not registered.\n''Invalid password, please give a password with a minimum length of 8 characters, at lease one capital letter and one special symbol\n'


# Test 5: Register new user with invalid password - below minimum length
def test_register_user_invalid_pw_too_short(mocker, temp_json, capsys):
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=['Jake', 'password123', 'y', 'Pass!23'])

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    login()
    captured_output = capsys.readouterr().out
    assert captured_output == 'User is not registered.\n''Invalid password, please give a password with a minimum length of 8 characters, at lease one capital letter and one special symbol\n'


# Test 6: Register new user with invalid password - no capital letter
def test_register_user_invalid_pw_no_capital(mocker, temp_json, capsys):
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=['Jake', 'password123', 'y', 'password123!'])

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    login()
    captured_output = capsys.readouterr().out
    assert captured_output == 'User is not registered.\n''Invalid password, please give a password with a minimum length of 8 characters, at lease one capital letter and one special symbol\n'


# Test 7: Register new user with invalid password - only blank space
def test_register_user_invalid_pw_blank_space(mocker, temp_json, capsys):
    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_login.UserInterface.get_user_input",
        side_effect=['Jake', 'password123', 'y', ' '])

    mocker.patch(
        "assignment_1.online_shopping_cart.user.user_data.UserDataManager.USER_FILE_PATHNAME",
        temp_json)

    login()
    captured_output = capsys.readouterr().out
    assert captured_output == 'User is not registered.\n''Invalid password, please give a password with a minimum length of 8 characters, at lease one capital letter and one special symbol\n'



def test_user_login8():
    # NOTE: Rename function to something appropriate
    pass


def test_user_login9():
    # NOTE: Rename function to something appropriate
    pass


def test_user_login10():
    # NOTE: Rename function to something appropriate
    pass