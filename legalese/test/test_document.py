import unittest
from legalese import Patch
from legalese import Document

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
        assert docs.values()[0] == None



