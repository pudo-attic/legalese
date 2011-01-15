from lxml import etree

class Patch():
    def __init__(self, element):
        self.element = element

    @property
    def document_name(self):
        return self.element.get('document')

    def apply(self, store):
        document = store.get(self.document_name)
        return {self.document_name: document}

