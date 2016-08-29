import logging


from iostest import app_locators


def test_landing(setup):
    logging.info("Finding element")
    by = setup.driver.find_element_by_xpath
    release_text = by(app_locators.text_release_notes)
    setup.soft_assert.assert_equals("Caption on landing page is incorrect", release_text.get_attribute("name"),
                                    "Release Notes")


def test_landing_on_main_page(setup):
    logging.info("Finding element")
    by = setup.driver.find_element_by_xpath
    release_text = by(app_locators.text_release_notes)
    setup.soft_assert.assert_equals("Caption on landing page is incorrect", release_text.get_attribute("name"),
                                    "Release Notes")
    button_done = by(app_locators.button_done)
    logging.info("Clicking Done for release notes")
    button_done.click()

    main_text = by(app_locators.text_main_view)
    setup.soft_assert.assert_equals("Caption on main page is incorrect", main_text.get_attribute("name"),
                                    "Card Decks")
