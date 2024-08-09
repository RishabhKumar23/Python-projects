#NOTE - Extract Tables from PDFs

# pip install ghostscript => in terminal

import camelot

table = camelot.read_pdf('file_name', pages='1')
print(table)

table.export('new_file.csv', f='csv', compress=True)
table[0].to._csv('new_file.csv')
