import properties


def test_login_page_displayed(setup):
    login_page = setup.get_first_page()

    assert login_page.is_displayed()


def test_input_login(setup):
    login_page = setup.get_first_page()
    password_page = login_page.input_login_and_next(properties.app_login)

    assert password_page.is_displayed()


def test_input_password(setup):
    login_page = setup.get_first_page()
    password_page = login_page.input_login_and_next(properties.app_login)
    notes_page = password_page.input_password_and_submit(properties.app_password)

    assert notes_page.is_displayed()
