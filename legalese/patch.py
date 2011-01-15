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

	method = {
	    "after": target.addnext,
	    "before": target.addprevious,
	    "append": lambda text, children: target.append(children),
	    "prepend": lambda x: target.insert(0,x)
	}.get(operation.get("pos","append"))

	name = operation.get("pos", "append")
	if name == "after":
	    if operation.text:
		next = target.getnext()
		next.text = next.text + operation.text if next.text else operation.text
	    for elem in list(operation):
		target.addnext(elem)
	elif name == "before":
	    for elem in reversed(list(operation)):
		target.addprevious(elem)
	elif name == "append":
	    if operation.text:
		last = list(target)[-1]
		last.text = last.text + operation.text if last.text else operation.text
	    for elem in list(operation):
		target.addnext(elem)
	elif name == "prepend":
	    pass
	else:
	    raise ValueError()








