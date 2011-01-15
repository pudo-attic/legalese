import os
from lxml import etree

from patch import Patch


class Document(object):

    def __init__(self, document_id, element):
        self.id = document_id
        self.element = element

    @classmethod
    def from_file(cls, document_id, file_name):
        xml_doc = etree.parse(file_name)
        return cls(document_id, xml_doc)

    @classmethod
    def from_string(cls, document_id, string):
        xml_doc = etree.fromstring(string)
        return cls(document_id, xml_doc)


    @property
    def patches(self):
        ps = self.element.xpath('//patch[not(ancestor::patch)]')
        return [Patch(p) for p in ps]


