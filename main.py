from pybtex.database import BibliographyData
from pybtex.database.input import bibtex
from pybtex.database.output.bibtex import Writer

parser = bibtex.Parser()
bibdata = parser.parse_file('/home/harry/Documents/Articles/library.bib')

availableFields = set()
availablePersons = set()

for bib_id in bibdata.entries:
    p = bibdata.entries[bib_id].persons
    b = bibdata.entries[bib_id].fields
    availableFields |= b.keys()
    availablePersons |= p.keys()

newBib = BibliographyData()

for bib_id in bibdata.entries:
    persons = bibdata.entries[bib_id].persons
    fields = bibdata.entries[bib_id].fields
    new_bib_id = bib_id

    if 'author' in persons.keys() and 'year' in fields.keys():
        new_bib_id = ''.join(a.last()[0] for a in persons['author'])
        new_bib_id += fields['year']

    newBib.entries[new_bib_id] = bibdata.entries[bib_id]

writer = Writer()
writer.write_file(newBib, '/home/harry/Documents/Articles/library_modKeys.bib')
