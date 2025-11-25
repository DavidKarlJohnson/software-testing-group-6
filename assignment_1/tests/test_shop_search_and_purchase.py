import pytest

from assignment_1.online_shopping_cart.shop import shop_search_and_purchase as ssp


def make_input(seq):
    it = iter(seq)

    def _inp(prompt):
        return next(it)

    return _inp


def test_search_and_purchase_all_path(monkeypatch):
    # login succeeds immediately, user searches 'all' then confirms
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'u', 'wallet': 0.0})
    called = {'csv': 0, 'filtered': 0, 'checkout': None}

    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: called.__setitem__('csv', called['csv'] + 1))
    monkeypatch.setattr(ssp, 'display_filtered_table', lambda *a, **k: called.__setitem__('filtered', called['filtered'] + 1))

    def fake_checkout(*a, **kw):
        called['checkout'] = kw.get('login_info', a[0] if a else None)

    monkeypatch.setattr(ssp, 'checkout_and_payment', fake_checkout)
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['all', 'y']))

    ssp.search_and_purchase_product()

    assert called['csv'] == 1
    assert called['filtered'] == 0
    assert called['checkout'] == {'username': 'u', 'wallet': 0.0}


def test_search_and_purchase_login_retry(monkeypatch):
    # login returns None first, then returns login info
    calls = {'count': 0}

    def fake_login():
        calls['count'] += 1
        return None if calls['count'] == 1 else {'username': 'retry', 'wallet': 1.0}

    monkeypatch.setattr(ssp, 'login', fake_login)
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: None)
    monkeypatch.setattr(ssp, 'display_filtered_table', lambda search_target: None)
    monkeypatch.setattr(ssp, 'checkout_and_payment', lambda *a, **kw: None)
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['all', 'y']))

    ssp.search_and_purchase_product()
    assert calls['count'] == 2


def test_search_and_purchase_filtered_search(monkeypatch):
    # search target other than 'all' uses display_filtered_table
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'u2', 'wallet': 5.0})
    recorded = {}

    def fake_filtered(search_target):
        recorded['search'] = search_target

    monkeypatch.setattr(ssp, 'display_filtered_table', lambda *a, **k: fake_filtered(*a, **k))
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: None)
    monkeypatch.setattr(ssp, 'checkout_and_payment', lambda *a, **kw: None)
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['Phone', 'y']))

    ssp.search_and_purchase_product()
    assert recorded['search'] == 'phone'


def test_search_and_purchase_ready_no_then_yes(monkeypatch):
    # user says not ready first, then ready; display called twice
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'u3'})
    counts = {'csv': 0}
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: counts.__setitem__('csv', counts['csv'] + 1))
    monkeypatch.setattr(ssp, 'display_filtered_table', lambda *a, **k: None)
    monkeypatch.setattr(ssp, 'checkout_and_payment', lambda *a, **kw: None)
    # Sequence: all, n, all, y
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['all', 'n', 'all', 'y']))

    ssp.search_and_purchase_product()
    assert counts['csv'] == 2


def test_search_and_purchase_case_insensitive_all(monkeypatch):
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'u4'})
    called = {'csv': 0}
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: called.__setitem__('csv', called['csv'] + 1))
    monkeypatch.setattr(ssp, 'checkout_and_payment', lambda login_info: None)
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['All', 'y']))

    ssp.search_and_purchase_product()
    assert called['csv'] == 1


def test_search_and_purchase_checkout_receives_login(monkeypatch):
    login_info = {'username': 'buyer', 'wallet': 2.0}
    monkeypatch.setattr(ssp, 'login', lambda: login_info)
    received = {}

    def fake_checkout(*a, **kw):
        received['li'] = kw.get('login_info', a[0] if a else None)

    monkeypatch.setattr(ssp, 'checkout_and_payment', fake_checkout)
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: None)
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['all', 'y']))

    ssp.search_and_purchase_product()
    assert received['li'] is login_info


def test_search_and_purchase_multiple_searches(monkeypatch):
    # several searches (filtered/all) then purchase; ensure checkout called once
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'multi'})
    calls = {'checkout': 0}
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: None)
    monkeypatch.setattr(ssp, 'display_filtered_table', lambda *a, **kw: None)

    def fake_checkout(*a, **kw):
        calls['checkout'] += 1

    monkeypatch.setattr(ssp, 'checkout_and_payment', fake_checkout)
    # Sequence: phone,n,all,n,phone,y
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['phone', 'n', 'all', 'n', 'phone', 'y']))

    ssp.search_and_purchase_product()
    assert calls['checkout'] == 1


def test_search_and_purchase_trim_and_case(monkeypatch):
    # inputs with surrounding spaces and mixed case are lowercased by function
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'spacecase'})
    recorded = {}
    monkeypatch.setattr(ssp, 'display_filtered_table', lambda *a, **k: recorded.setdefault('val', k.get('search_target', a[0] if a else None)))
    monkeypatch.setattr(ssp, 'checkout_and_payment', lambda *a, **kw: None)
    # input has spaces and caps
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['  Phone  ', 'y']))

    ssp.search_and_purchase_product()
    # note: function calls .lower() but does not strip; therefore expected lowercased with spaces
    assert recorded['val'] == '  phone  '


def test_search_and_purchase_accepts_yes_variants(monkeypatch):
    # 'yes' should startwith 'y' and be accepted
    monkeypatch.setattr(ssp, 'login', lambda: {'username': 'yesman'})
    monkeypatch.setattr(ssp, 'display_csv_as_table', lambda: None)
    called = {'checkout': False}
    monkeypatch.setattr(ssp, 'checkout_and_payment', lambda *a, **kw: called.__setitem__('checkout', True))
    monkeypatch.setattr(ssp.UserInterface, 'get_user_input', make_input(['all', 'yes']))

    ssp.search_and_purchase_product()
    assert called['checkout'] is True