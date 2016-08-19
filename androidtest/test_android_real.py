def test_caption(setup):
    el = setup.driver.find_element_by_android_uiautomator("new UiSelector().text(\"Заметки\")")

    assert el.is_displayed()


def test_go_to_reminders(setup):
    menu = setup.driver.find_element_by_android_uiautomator(
        "new UiSelector().description(\"Открыть панель навигации\")")
    menu.click()

    reminders_menu_item = setup.driver.find_element_by_id('com.google.android.keep:id/drawer_navigation_reminders')
    reminders_menu_item.click()

    reminders_caption = setup.driver.find_element_by_android_uiautomator("new UiSelector().text(\"Напоминания\")")

    assert reminders_caption.is_displayed()
