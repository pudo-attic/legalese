# encoding: utf-8
from lxml import etree
from copy import deepcopy

from xml.dom.minidom import parse, parseString

class Patch():
    def __init__(self, element):
        self.element = element

    @property
    def dom(self):
	if self._dom is None:
	    self._dom
	return self._dom


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
            for elem in reversed(list(change)):
                target.addnext(elem)
	    target.tail = change.text
        elif name == "before":
            if change.text:
		if target.getprevious() is not None:
		    prev = target.getprevious()
		    prev.tail = prev.tail + change.text if prev.tail else change.text
		else:
		    par = target.getparent()
		    par.text = par.text + change.text if par.text else change.text
            for elem in list(change):
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
	    if len(list(change)):
		last = list(change)[-1]
		last.tail = (last.tail or "") + (target.text or "")
		target.text = change.text
	    else:
		target.text = change.text + target.text

            for elem in reversed(list(change)):
                target.insert(0, elem)

        else:
            raise ValueError()








