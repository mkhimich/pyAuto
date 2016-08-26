import logging


class BaseElement(object):
    def __init__(self, element):
        self.element = element

    def is_displayed(self):
        logging.info("Checking if element is DISPLAYED " + self.element.selector)
        return self.element.is_displayed()


class Text(BaseElement):
    def get_text(self):
        logging.info("Executing element GET TEXT " + self.element.selector)
        return self.element.text


class Button(Text):
    def click(self):
        logging.info("Executing element CLICK " + self.element.selector)
        return self.element.click()


class EditField(BaseElement):
    def get_value(self):
        logging.info("Getting element VALUE " + self.element.selector)
        return self.element.value

    def clear(self):
        logging.info("Executing element CLEAR " + self.element.selector)
        self.element.clear()

    def type_text(self, text):
        logging.info("Executing element SEND KEYS " + self.element.selector)
        self.element.send_keys(text)

    def set_text(self, text):
        self.clear()
        self.type_text(text)
