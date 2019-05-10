#CSV to Latex
import csv
from pylatex import Document, Tabular, Section

# Open the csv and also the latex files
def csv2tex(filename):
    doc = Document()
    with open('../Test_Files/' +filename+'.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        # get each row and convert it to Latex
        header = next(reader)
        size = '|l'*len(header)
        size = size + '|'

        #print(type(size))
        with doc.create(Tabular(size)) as table:
            table.add_hline()
            table.add_row(header)
            table.add_hline()
            for row in reader:
                table.add_row(row)
                table.add_hline()
    doc.generate_tex(filename)

#test area
if __name__ == "__main__":
    csv2tex('test')
