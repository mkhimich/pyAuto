# coding=utf-8
from datetime import datetime

import pytest

dt = datetime.now()
time = str(dt.microsecond)
note_title = 'Note Title ' + time
note_text = 'Note Text ' + time
note_title_edited = 'Edited Note Title ' + time
note_text_edited = 'Edited Note Text ' + time


def test_keep_create(setup):
    create_note(note_title, note_text, setup)

    open_note(note_title, setup)

    verify_note(note_title, note_text, setup)


def test_keep_edit(setup):
    open_note(note_title, setup)

    update_note(note_title_edited, note_text_edited, setup)

    open_note(note_title_edited, setup)

    verify_note(note_title_edited, note_text_edited, setup)


def test_keep_delete(setup):
    open_note(note_title_edited, setup)

    setup.driver.find_element_by_id("com.google.android.keep:id/bs_action_button").click()
    setup.driver.find_element_by_android_uiautomator(
        "new UiSelector().resourceId(\"com.google.android.keep:id/menu_text\").text(\"Delete\")").click()

    selector = "new UiSelector().resourceId(\"com.google.android.keep:id/title\").text(\"{}\")".format(
        note_title_edited)
    assert len(setup.driver.find_elements_by_android_uiautomator(selector)) == 0


def open_note(note_title_to_find, setup):
    for note in setup.driver.find_elements_by_id("com.google.android.keep:id/title"):
        if note.text == note_title_to_find:
            note.click()
            return
        else:
            pytest.fail("Note wasn't found")


def create_note(note_title_to_set, note_text_to_set, setup):
    setup.driver.find_element_by_id("com.google.android.keep:id/new_note_button").click()
    set_title(note_title_to_set, setup)
    set_note(note_text_to_set, setup)
    setup.driver.find_element_by_android_uiautomator("new UiSelector().description(\"Open navigation drawer\")").click()


def update_note(note_title_to_set, note_text_to_set, setup):
    set_title(note_title_to_set, setup)
    set_note(note_text_to_set, setup)
    setup.driver.find_element_by_android_uiautomator("new UiSelector().description(\"Open navigation drawer\")").click()


def set_title(note_title_to_set, setup):
    element = setup.driver.find_element_by_id("com.google.android.keep:id/editable_title")
    element.click()
    element.clear()
    element.send_keys(note_title_to_set)


def set_note(note_text_to_set, setup):
    element = setup.driver.find_element_by_id("com.google.android.keep:id/edit_note_text")
    element.click()
    element.clear()
    element.send_keys(note_text_to_set)


def verify_note(note_title_to_verify, note_text_to_verify, setup):
    assert setup.driver.find_element_by_id("com.google.android.keep:id/editable_title").text == note_title_to_verify
    assert setup.driver.find_element_by_id("com.google.android.keep:id/edit_note_text").text == note_text_to_verify
