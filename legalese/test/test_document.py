# encoding: utf-8
import unittest
from lxml import etree
from legalese import Patch
from legalese import Document
from re import sub

class TestDocument(unittest.TestCase):

    def setUp(self):
        fn = "fixtures/VFUIK2009.xml"
        self.document = Document.from_file("TESTFOO", fn)

    def test_loading_from_file(self):
        assert isinstance(self.document, Document)
        assert self.document.id == "TESTFOO"
        assert not len(self.document.patches)

    def test_should_explode_when_root_is_not_document(self):
	self.assertRaises(AssertionError, Document.from_string, "foo", """<something></something>""")

    def test_empty_doc_should_return_root_for_lookup(self):
        document = Document.empty("id")
	assert document.lookup("") is not None


    def test_lookup(self):
	assert self.document.lookup_text("").startswith("Verordnung")
	assert self.document.lookup_text("p1").startswith("Umlagesatz")
	assert self.document.lookup_text("p2").startswith("Inkrafttreten")
	assert self.document.lookup_text("p1/s1") is None
	assert self.document.lookup_text("p2/s1").startswith("Diese Verordnung tritt")

    def test_loading_document_from_string(self):
        doc = Document.from_string("foo", """<document></document>""")
        assert isinstance(doc, Document)


class TestDocumentWithPatches(unittest.TestCase):
    def setUp(self):
        fn = "fixtures/with_patches.xml"
        self.document = Document.from_file("FOO", fn)

    def test_find_patches(self):
        ps = self.document.patches
        assert len(ps) == 2
        assert ['test_document', 'document4'] == [p.document_name for p in ps]


class TestPatch(unittest.TestCase):
    def test_apply_patch(self):
        patch = Document.from_string("foo", """<document><patch document="example"></patch></document>""").patches[0]
        docs = patch.apply({})
        assert len(docs.keys()) == 1
        assert docs.keys()[0] == 'example'

    def test_apply_create_patch(self):
	patch = Document.from_file(None, "fixtures/patch_create.xml").patches[0]
	docs = patch.apply({})
	doc = docs.values()[0]

	assert docs.keys()[0] == "example_doc"
	assert isinstance(doc, Document)
	assert doc.lookup_text("p1").startswith("I exist")
	assert doc.lookup_text("p2").startswith("This exists")

    def test_append_patch(self):
	patch = Document.from_file(None, "fixtures/patch_add.xml").patches[0]
	original_doc = Document.from_file("example_doc", "fixtures/patch_template.xml")
	docs = patch.apply({"example": original_doc})
	doc = docs.values()[0]

	actual = etree.tostring(doc.lookup(""))
	expected = open("fixtures/patch_expected.xml").read()
	#print sub("\\s+"," ", actual).strip()
	#print sub("\\s+", " ", expected).strip()
	assert sub("\s+"," ", actual).strip() == sub("\s+", " ", expected).strip()


