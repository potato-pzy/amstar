import PyPDF2
reader = PyPDF2.PdfReader('Blogs-1.pdf')
text = reader.pages[0].extract_text()
# Replace '\n \n \n' with a unique token for paragraph
text = text.replace('\n \n \n', '<PARA>')
# Replace '\n \n' with space
text = text.replace('\n \n', ' ')
# Replace single '\n' with space (if any)
text = text.replace('\n', '')

print(text[:1000])
