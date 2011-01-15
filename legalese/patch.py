# encoding: utf-8
from lxml import etree
from copy import deepcopy

class Patch():
    def __init__(self, element):
        self.element = element

    @property
    def document_name(self):
        return self.element.get('document')

    def apply(self, store):
	ops = {"add": self._add}

	from document import Document
        document = store.get(self.document_name)
	if document is None:
	    document = Document.empty(self.document_name)

	for operation in self.element.iterchildren():
	    op = ops.get(operation.tag)
	    op(document, operation)

        return {self.document_name: document}



    def _add(self, document, operation):
	target_path = operation.get("at")
	target = document.lookup(target_path)
	for node in operation.iterchildren():
	    target.append(node)




