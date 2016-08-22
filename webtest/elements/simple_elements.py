class BaseElement(object):
    def __init__(self, element):
        self.element = element

    def is_displayed(self):
        return self.element.is_displayed()


class Text(BaseElement):
    def get_text(self):
        return self.element.text


class Button(Text):
    def click(self):
        return self.element.click()


class EditField(BaseElement):
    def get_value(self):
        return self.element.value

    def clear(self):
        self.element.clear()

    def type_text(self, text):
        self.element.send_keys(text)

    def set_text(self, text):
        self.clear()
        self.type_text(text)
