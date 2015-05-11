import zipfile
from lxml import etree

ns = {
    'n':'urn:oasis:names:tc:opendocument:xmlns:container',
    'pkg':'http://www.idpf.org/2007/opf',
    'dc':'http://purl.org/dc/elements/1.1/'
}

def to_dict(t, serialize):
    """ customize etree element to dictionary
    Args:
         t: etree element
         serialize : map (from-etree-attr, to-dict-key, [string-format] )
            ex: ('href', 'path', 'd:\epub\%s'), ('media-type': 'media_type')]
             -> {'path': 'd:\epub\toc.html', 'media-type':'html'}
    """
    res = {}
    try:
        for e in serialize:
            if len(e) < 3:
                res.update({e[1]: t.attrib[e[0]]})
            else:
                res.update({e[1]: e[2]%(t.attrib.get(e[0]))})
    except Exception, er:
        print er
    return res

def etree_to_dict(t):
    """ default extract all xml node to dict
    """
    #d = {t.tag : map(etree_to_dict, t.iterchildren())}
    val = {}
    val.update(((k, v) for k, v in t.attrib.iteritems()))
    d = {t.xpath('local-name()') : val}
    # want to extract text ? uncomment this line
    #d['text'] = t.text
    return d


class Pyepub():
    """ extract epub verison 2 and  version 3 information """
    def __init__(self, tree):
        self.tree = tree

    @classmethod
    def from_filename(cls, filename):
        # prepare to read from the .epub file
        zip = zipfile.ZipFile(filename)
        return cls._read_zip(zip)

    @classmethod
    def from_zip_file(cls, zipfile):
        return cls._read_zip(zipfile)

    @property
    def metadata(self):
        metadata = self.tree.xpath('/pkg:package/pkg:metadata',namespaces=ns)[0]
        v3 = ['contributor', 'coverage' , 'creator' , 'date' , 'description' , 'format' , 'identifier' , 'language' , 'publisher' , 'relation' , 'rights' , 'source' , 'subject' , 'title' , 'type']
        res = {}
        for s in v3:
            t = metadata.xpath('dc:%s/text()'%(s),namespaces=ns)
            if len(t) == 1:
                res[s] = t[0]
            elif len(t) > 1:
                res[s] = [item for item in t]

        return res

    @property
    def epub_version(self):
        version = self.tree.xpath('/pkg:package/@version', namespaces=ns)
        return version

    @property
    def cover(self):
        # prediction only
        caddiate = self.tree.xpath('/pkg:package/pkg:manifest/pkg:item[@media-type="image/jpeg"]',namespaces=ns)
        for c in caddiate:
            for k, v in c.attrib.iteritems():
                if v.find('cover') != -1:
                    return c.attrib['href']
        return None

    def manifest(self, serialize=None):
        manifesttree = self.tree.xpath('/pkg:package/pkg:manifest',namespaces=ns)[0]
        if serialize is None:
            manifest = [etree_to_dict(item) for item  in manifesttree  if isinstance(item, etree._Comment)  == False]
        else:
            manifest = [to_dict(item, serialize) for item  in manifesttree if isinstance(item, etree._Comment)  == False]
        return manifest


    def spine(self, serialize=None):
        spinetree = self.tree.xpath('/pkg:package/pkg:spine',namespaces=ns)[0]
        if serialize is None:
            spine = [etree_to_dict(item) for item  in spinetree  if isinstance(item, etree._Comment) == False]
        else:
            spine = [to_dict(item, serialize) for item  in spinetree  if isinstance(item, etree._Comment) == False]
        return spine


    def guide(self, serialize=None):
        guide = []
        guidetree = self.tree.xpath('/pkg:package/pkg:guide',namespaces=ns)
        if len(guidetree) > 0:
            guidetree= guidetree[0]
            if serialize is None:
                guide = [etree_to_dict(item) for item  in guidetree  if isinstance(item, etree._Comment)  == False]
            else:
                guide = [to_dict(item, serialize) for item  in guidetree  if isinstance(item, etree._Comment)  == False]
        return guide

    @classmethod
    def _read_zip(cls, zip):
        # find the contents metafile
        txt = zip.read('META-INF/container.xml')
        tree = etree.fromstring(txt)
        cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path',namespaces=ns)[0]

        # grab the metadata block from the contents metafile
        cf = zip.read(cfname)
        tree = etree.fromstring(cf)
        epub = Pyepub(tree)
        epub.opf_file_path = cfname
        return epub
