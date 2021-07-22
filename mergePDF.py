import PyPDF2
import os

pdf_loc = r'../'

pdf_file = ['*.pdf']

for _ in range(len(pdf_file)):
    file = os.path.join(pdf_loc, pdf_file[_])
    pdf_file[_] = open(file, 'rb')

merged_pdf = PyPDF2.PdfFileWriter()

for pdfs in pdf_file:
    pdf = PyPDF2.PdfFileReader(pdfs)
    for page in pdf.pages:
        merged_pdf.addPage(page)

new_merged_pdf = os.path.join(pdf_loc, 'merged_pdf.pdf')
new_merged_pdf_descriptor = open(new_merged_pdf, 'wb')

merged_pdf.write(new_merged_pdf_descriptor)

for pdf_descriptor in pdf_file:
    pdf_descriptor.close()
    
new_merged_pdf_descriptor.close()
