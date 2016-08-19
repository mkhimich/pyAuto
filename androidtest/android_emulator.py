def test_find_elements(setup):
    el = setup.driver.find_element_by_accessibility_id('Graphics')
    el.click()
    el = setup.driver.find_element_by_accessibility_id('Arcs')
    assert el is not None

    setup.driver.back()

    el = setup.driver.find_element_by_accessibility_id("App")
    assert el is not None

    els = setup.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
    assert 12 >= len(els)

    setup.driver.find_element_by_android_uiautomator('text("API Demos")')


def test_simple_actions(setup):
    el = setup.driver.find_element_by_accessibility_id('Graphics')
    el.click()

    el = setup.driver.find_element_by_accessibility_id('Arcs')
    el.click()

    setup.driver.find_element_by_android_uiautomator('new UiSelector().text("Graphics/Arcs")')
