import os
import unittest
from lxml import etree


class Document(object):
    
    def __init__(self, document_id, element):
        self.id = document_id
        self.element = element

    @classmethod
    def from_file(cls, document_id, file_name):
        xml_doc = etree.parse(file_name)
        return cls(document_id, xml_doc)

    @property
    def patches(self):
        ps = self.element.xpath('//patch[not(ancestor::patch)]')
        return [Patch(p) for p in ps]


class Patch():
    
    def __init__(self, element):
        self.element = element
    
    @classmethod
    def from_string(cls, string):
        doc = etree.fromstring(string)
        return cls(doc) 

    @property
    def document_name(self):
        return self.element.get('document')

    def apply(self, store): 
        document = store.get(self.document_name)
        return {self.document_name: document}

class TestDocument(unittest.TestCase):
    
    def setUp(self):
        fn = "fixtures/VFUIK2009.xml"
        self.document = Document.from_file("TESTFOO", fn)

    def test_loading_from_file(self):
        assert isinstance(self.document, Document)
        assert self.document.id == "TESTFOO"
        assert not len(self.document.patches)


class TestDocumentWithPatches(unittest.TestCase):

    def setUp(self):
        fn = "fixtures/with_patches.xml"
        self.document = Document.from_file("FOO", fn)

    def test_find_patches(self):
        ps = self.document.patches
        assert len(ps) == 2
        assert ['test_document', 'document4'] == [p.document_name for p in ps]
    

class TestPatch(unittest.TestCase):
    
    def test_loading_patch_from_string(self):
        patch = Patch.from_string("""<patch document="example"></patch>""")
        assert isinstance(patch, Patch)
        assert patch.document_name == 'example'
    
    def test_apply_patch(self):
        patch = Patch.from_string("""<patch document="example"></patch>""")
        docs = patch.apply({})
        assert len(docs.keys()) == 1
        assert docs.keys()[0] == 'example'
        assert docs.values()[0] == None

if __name__ == '__main__':
    unittest.main() 


