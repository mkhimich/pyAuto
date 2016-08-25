import properties


def test_input_login(setup):
    login_page = setup.get_first_page()
    password_page = login_page.input_login_and_next(properties.app_login)

    assert not password_page.is_displayed()


def test_input_password(setup):
    login_page = setup.get_first_page()
    password_page = login_page.input_login_and_next("test my spirit")
    notes_page = password_page.input_password_and_submit("rage!")

    assert notes_page.is_displayed()


def test_flaky_bitch(setup):
    from random import random
    assert random() > 0.5
