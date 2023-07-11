import PyPDF2

reader = PyPDF2.PdfReader('test.pdf')
n = len(reader.pages)
print(n)
pages = []
for i in range(n):
    pages.append(reader.pages[i])

with open('test.html', 'w', encoding='utf-8') as wf:
    for i in pages:
        wf.write(f'<pre>{i.extract_text()}</pre>')
