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


def test_add_label_menu_item_present(setup):
    login_page = setup.get_first_page()
    password_page = login_page.input_login_and_next(properties.app_login)
    notes_page = password_page.input_password_and_submit(properties.app_password)

    assert notes_page.get_create_new_label_menu_item().is_displayed()


def test_add_label_dialog(setup):
    password_page = setup.get_first_page().input_login_and_next(properties.app_login)
    notes_page = password_page.input_password_and_submit(properties.app_password)
    edit_labels_dialog = notes_page.click_new_label_menu_item()

    assert edit_labels_dialog.is_displayed()


def test_create_label(setup):
    password_page = setup.get_first_page().input_login_and_next(properties.app_login)
    notes_page = password_page.input_password_and_submit(properties.app_password)
    edit_labels_dialog = notes_page.click_new_label_menu_item()

    from random import random
    label_name = "ew_label_" + str(random())
    edit_labels_dialog.create_label(label_name)
    edit_labels_dialog.get_done_button().click()

    notes_page.get_menu_button().click()
    assert notes_page.wait_if_element_visible(notes_page.get_label_menu_item(label_name))


def test_delete_label(setup):
    password_page = setup.get_first_page().input_login_and_next(properties.app_login)
    notes_page = password_page.input_password_and_submit(properties.app_password)
    edit_labels_dialog = notes_page.click_new_label_menu_item()

    from random import random
    label_name = "del_label_" + str(random())
    edit_labels_dialog.create_label(label_name)
    edit_labels_dialog.delete_first_label()
    edit_labels_dialog.get_done_button().click()

    notes_page.get_menu_button().click()
    assert not notes_page.if_label_menu_item_present(label_name)
