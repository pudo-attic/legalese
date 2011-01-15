# encoding: utf-8
import os
from lxml import etree

from patch import Patch


class Document(object):
    def __init__(self, document_id, element):
	assert element.tag == "document"
        self.id = document_id
        self.element = element

    def lookup(self, path):
	xpath = "/".join(["*[@ref='%s']" % s for s in path.split("/") if len(s)])
	if len(xpath) == 0:
	    return self.element

	return self.element.find(xpath)

    def lookup_text(self, path):
	node = self.lookup(path)
	if node is not None:
	    return node.xpath("string()").strip()


    @classmethod
    def from_file(cls, document_id, file_name):
        xml_doc = etree.parse(file_name).getroot()
        return cls(document_id, xml_doc)

    @classmethod
    def from_string(cls, document_id, string):
        xml_doc = etree.fromstring(string)
        return cls(document_id, xml_doc)

    @classmethod
    def empty(cls, document_id):
	return cls.from_string(document_id, "<document></document>")

    @property
    def patches(self):
        ps = self.element.xpath('//patch[not(ancestor::patch)]')
        return [Patch(p) for p in ps]


