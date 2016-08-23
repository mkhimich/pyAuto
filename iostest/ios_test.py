import datetime
import logging


from iostest import app_locators


def test_get_url(setup):
    logging.info("Finding element")
    by = setup.driver.find_element_by_xpath
    release_text = by(app_locators.text_release_notes)
    assert release_text.get_attribute("name") == "Release Notes"
    button_done = by(app_locators.button_done)
    logging.info("Clicking Done for release notes")
    button_done.click()

    main_text = by(app_locators.text_main_view)
    assert main_text.get_attribute("name") == "Card Decks"

