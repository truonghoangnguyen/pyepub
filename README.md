# pyepub
Python library to extract epub information

## quick using example:
```
import pyepub

epub = pyepub.Pyepub.from_filename('fname.epub')
# get metadata
metadata = epub.metadata

# get manifest
manifest = epub.manifest()
# outut: [{'item': {'href': 'part.html', 'media-type': 'application/xhtml+xml'}}]

# custimize get mainfest
serialize = [('href', 'path', 'LOCAL_HOST/%s'), ('media-type', 'media-type')]
manifest = epub.manifest(serialize)
# outut: [{'href': 'LOCAL_HOST/part.html', 'media-type': 'application/xhtml+xml'}]
```        
