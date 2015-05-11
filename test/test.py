
import unittest
import  os, sys
base_dir = os.path.dirname(os.getcwd())
sys.path.append(base_dir)
sys.path.append(base_dir + '..')

import zipfile
import pyepub


class TestCaribe(unittest.TestCase):
    def setUp(self):
        #fname = 'cho_toi_xin_mot_ve_di_tuoi_tho__nguyen_nhat_anh.epub'
        fname = 'moby-dick.epub'
        #fname = 'Calibre Quick Start Guide - John Schember.epub'
        self.epub = pyepub.Pyepub.from_filename(fname)
        zip = zipfile.ZipFile(fname)
        self.epub_zip = pyepub.Pyepub.from_zip_file(zip)

    def test_zip(self):
        m1 = self.epub.manifest()
        m2 = self.epub_zip.manifest()
        self.assertEqual(m1, m2)

    def test_manifest(self):
        m1 = self.epub.manifest()
        serialize = [('href', 'path', 'nguyen/%s'), ('media-type', 'media-type')]
        m2 = self.epub.manifest(serialize)
        self.assertEqual(len(m1), len(m2))

    def test_spine(self):
        m1 = self.epub.spine()
        serialize = [('idref', 'path', 'ngueb%s')]
        m2 = self.epub.spine(serialize)
        self.assertEqual(len(m1), len(m2))

    def test_guide(self):
        m1 = self.epub.guide()
        serialize = [('href', 'pathzxx', 'ngueb/%s')]
        m2 = self.epub.guide(serialize)
        self.assertEqual(len(m1), len(m2))

    def test_print(self):
        #print self.epub.metadata
        serialize = [('href', 'path', 'nguyen/%s'), ('media-type', 'media-type')]
        print self.epub.manifest(serialize)

if __name__ == '__main__':
    unittest.main()

