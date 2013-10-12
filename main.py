from BibTexUtils import BibTexReader

reader = BibTexReader(None, '/home/harry/Documents/Articles/library.bib')

reader.read()
print(reader.bibdata)
print(reader.fields)
print(reader.persons)
print(reader.bibtexfile)
