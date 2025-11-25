import pytest

from assignment_1.online_shopping_cart.shop import shop_search_and_purchase as ssp


def make_input(seq):
    it = iter(seq)

    def _inp(prompt):
        return next(it)

    return _inp


def test_search_and_purchase_all_path(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'u', 'wallet': 0.0})
    called = {'csv': 0, 'filtered': 0, 'checkout': None}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: called.__setitem__('csv', called['csv'] + 1))
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table', new=lambda *a, **k: called.__setitem__('filtered', called['filtered'] + 1))

    def fake_checkout(*a, **kw):
        called['checkout'] = kw.get('login_info', a[0] if a else None)

    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=fake_checkout)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['all', 'y'])

    ssp.search_and_purchase_product()

    assert called['csv'] == 1
    assert called['filtered'] == 0
    assert called['checkout'] == {'username': 'u', 'wallet': 0.0}


def test_search_and_purchase_login_retry(mocker):
    calls = {'count': 0}

    def fake_login():
        calls['count'] += 1
        return None if calls['count'] == 1 else {'username': 'retry', 'wallet': 1.0}

    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', new=fake_login)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table', new=lambda *a, **kw: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=lambda *a, **kw: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['all', 'y'])

    ssp.search_and_purchase_product()
    assert calls['count'] == 2


def test_search_and_purchase_filtered_search(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'u2', 'wallet': 5.0})
    recorded = {}

    def fake_filtered(search_target):
        recorded['search'] = search_target

    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table', new=lambda *a, **kw: fake_filtered(*a, **kw))
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=lambda *a, **kw: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['Phone', 'y'])

    ssp.search_and_purchase_product()
    assert recorded['search'] == 'phone'


def test_search_and_purchase_ready_no_then_yes(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'u3'})
    counts = {'csv': 0}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: counts.__setitem__('csv', counts['csv'] + 1))
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table', new=lambda *a, **k: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=lambda *a, **kw: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['all', 'n', 'all', 'y'])

    ssp.search_and_purchase_product()
    assert counts['csv'] == 2


def test_search_and_purchase_case_insensitive_all(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'u4'})
    called = {'csv': 0}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: called.__setitem__('csv', called['csv'] + 1))
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=lambda *a, **kw: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['All', 'y'])

    ssp.search_and_purchase_product()
    assert called['csv'] == 1


def test_search_and_purchase_checkout_receives_login(mocker):
    login_info = {'username': 'buyer', 'wallet': 2.0}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value=login_info)
    received = {}

    def fake_checkout(*a, **kw):
        received['li'] = kw.get('login_info', a[0] if a else None)

    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=fake_checkout)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['all', 'y'])

    ssp.search_and_purchase_product()
    assert received['li'] is login_info


def test_search_and_purchase_multiple_searches(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'multi'})
    calls = {'checkout': 0}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table', new=lambda *a, **kw: None)

    def fake_checkout(*a, **kw):
        calls['checkout'] += 1

    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=fake_checkout)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['phone', 'n', 'all', 'n', 'phone', 'y'])

    ssp.search_and_purchase_product()
    assert calls['checkout'] == 1


def test_search_and_purchase_trim_and_case(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'spacecase'})
    recorded = {}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_filtered_table', new=lambda *a, **k: recorded.setdefault('val', k.get('search_target', a[0] if a else None)))
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=lambda *a, **kw: None)
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['  Phone  ', 'y'])

    ssp.search_and_purchase_product()
    assert recorded['val'] == '  phone  '


def test_search_and_purchase_accepts_yes_variants(mocker):
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.login', return_value={'username': 'yesman'})
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.display_csv_as_table', new=lambda: None)
    called = {'checkout': False}
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.checkout_and_payment', new=lambda *a, **kw: called.__setitem__('checkout', True))
    mocker.patch('assignment_1.online_shopping_cart.shop.shop_search_and_purchase.UserInterface.get_user_input', side_effect=['all', 'yes'])

    ssp.search_and_purchase_product()
    assert called['checkout'] is True