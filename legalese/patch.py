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

    def _add(self, document, change):
        target_path = change.get("at")
        target = document.lookup(target_path)

        name = change.get("pos", "append")
        if name == "after":
            if change.text:
                next = target.getprevious()
                next.text = next.text + change.text if next.text else change.text
            for elem in list(change):
                target.addnext(elem)
        elif name == "before":
            if change.text:
                next = target.getnext()
                next.text = change.text + next.text if next.text else change.text
            for elem in reversed(list(change)):
                target.addprevious(elem)
        elif name == "append":
            if change.text:
                if len(list(target)):
                    prev = list(target)[-1]
                    prev.tail = prev.tail + change.text if prev.tail else change.text
                else:
                    target.text = target.text + change.text if target.text else change.text
            for elem in list(change):
                target.append(elem)
        elif name == "prepend":
            if change.text:
                target.text = target.text + change.text if target.text else change.text
            for elem in reversed(list(change)):
                target.insert(0, elem)
        else:
            raise ValueError()








