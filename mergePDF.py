import PyPDF2
import os

pdf_loc = r'..\'

pdf_files = ['pdf01.pdf','pdf02.pdf']

pdf_records = []

for _ in range(len(pdf_files)):
    file = os.path.join(pdf_loc, pdf_files[_])
    # print('\nReading file - ',file)
    pdf_records.append(open(file, 'rb'))

print(f'\n{len(pdf_files)} files read.')

merged_pdf = PyPDF2.PdfFileWriter()

pdf_counter = 1
pdf_page_counter = 1
total_pages_counter = 0

print('\nBegin to merge pdfs.....')

for pdfs in pdf_records:
    print(f'\n\n* Combining pdf {pdf_files[pdf_counter-1]} {pdf_counter}/{len(pdf_files)}')
    pdf = PyPDF2.PdfFileReader(pdfs,strict=False)
    for page in pdf.pages:
        print(f'  - Combining pdf pages - Pages {pdf_page_counter}/{len(pdf.pages)}', end='\r')
        pdf_page_counter = pdf_page_counter + 1
        total_pages_counter = total_pages_counter + 1
        merged_pdf.addPage(page)
    pdf_counter = pdf_counter + 1
    pdf_page_counter = 1

print('\n\nAll pages read. Saving merged file.')

new_merged_pdf = os.path.join(pdf_loc, 'merged_pdf.pdf')
new_merged_pdf_descriptor = open(new_merged_pdf, 'wb')

merged_pdf.write(new_merged_pdf_descriptor)

for pdf_descriptor in pdf_records:
    pdf_descriptor.close()
    
new_merged_pdf_descriptor.close()

print(f'{len(pdf_files)} files merged and total {total_pages_counter} pages combines.')
