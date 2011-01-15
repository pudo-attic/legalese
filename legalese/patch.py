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

        name = operation.get("pos", "append")
        if name == "after":
            if operation.text:
                next = target.getprevious()
                next.text = next.text + operation.text if next.text else operation.text
            for elem in list(operation):
                target.addnext(elem)
        elif name == "before":
            if operation.text:
                next = target.getnext()
                next.text = operation.text + next.text if next.text else operation.text
            for elem in reversed(list(operation)):
                target.addprevious(elem)
        elif name == "append":
            if operation.text:
                if len(list(target)):
                    prev = list(target)[-1]
                    prev.tail = prev.tail + operation.text if prev.tail else operation.text
                else:
                    target.text = target.text + operation.text if target.text else operation.text
            for elem in list(operation):
                target.append(elem)
        elif name == "prepend":
            if operation.text:
                target.text = target.text + operation.text if target.text else operation.text
            for elem in reversed(list(operation)):
                target.insert(0, elem)
        else:
            raise ValueError()








