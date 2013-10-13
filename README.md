BibKeyChanger
=============
This is just a tiny program that allows to adapt all keys in a BibTex file according to a selected pattern.

You start by opening a BibTex file. That will lead to a list of all available BibTex data fields (set union, that does
not mean that all entries actually have all those keys), as well as the file being shown in the GUI. You can then click
on any number of fields in the list view which will generate a key pattern in exactly that order. Then you can click
on 'Preview' to see how the keys would look like, and if you are satisfied with the result, you can save it to a BibTex
file again.

You need the following to run the program:

1. Pybtex: http://pybtex.sourceforge.net/
2. PyQt5: http://pyqt.sourceforge.net/Docs/PyQt5/introduction.html
