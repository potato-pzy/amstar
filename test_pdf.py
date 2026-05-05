import PyPDF2
reader = PyPDF2.PdfReader('Blogs-1.pdf')
print(repr(reader.pages[0].extract_text()[:500]))
