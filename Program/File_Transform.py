import csv
import urllib.request
from time import sleep
from pathlib import Path
from bs4 import BeautifulSoup as bs
from pylatex import Document, Tabular, Section
from icalendar import Calendar, vDatetime


class Transformer:
    def __init__(self):
        self.table = [] #* Table that will store the parsed table in the same format for all data types
    '''-------------------------------------------------------------------------
    ##---------------------- Start Supporting Functions ----------------------##
    -------------------------------------------------------------------------'''

    #{Function:------------------------------------------------------------------------##
    #---------- Pick a table from the list of tables sent ----------------------------}##
    def pick_table(self, tables):
        print("*"*80,
                    "\nFrom below pick the table you want")
        print("*"*80)
        i = 1
        # Display all the current tables numbered
        for table in tables:
            print('[',i,']:')
            for row in table:
                print('|'.join(row))
                i += 1
        print("*"*80)
        usrIn = input("Enter Choice:")
        # Update Table with the
        try:
            x = int(usrIn)
            if x <= len(tables):
                self.table = tables[x-1]
            else:
                raise ValueError
        except ValueError:
            print("Did not enter the right number")

    #{Function:------------------------------------------------------------------------##
    #---------- Pick a table from the list of tables sent ----------------------------}##
    def html_data(self):
        html = ['<!-DOCTYPE html>\n<html>\n\t<style>table, th, td { border: 1px solid black; border-collapse: collapse; }</style>\n\t<body>\n\t\t<table>\n']
        end = '\t\t</table>\n\t</body>\n</html>'

        th = ""
        for row in self.table:
            html.append('\t\t\t<tr>\n')
            if th == "":
                th = '1'
                for col in row:
                    if ''.join(row).replace(' ', '') == '': break
                    html.append('\t\t\t\t<th>'+col+'</th>\n')
            else:
                for col in row:
                    html.append('\t\t\t\t<td>'+col+'</td>\n')
            html.append('\t\t\t</tr>\n')
        html.append(end)
        return ''.join(html)

    ## Sub if the file exists as html or eml
    def file_check(self, filename):
        try:
            page = "" #Store the data read from files

            # Treat filename as webpage if file isn't eml/html
            if Path('../Test_Files/'+filename+".html").is_file():
                with open('../Test_Files/'+filename+'.html') as nf:
                    page = nf.read()
            elif Path('../Test_Files/'+filename+".eml").is_file():
                with open('../Test_Files/'+filename+'.eml') as nf:
                    page = nf.read()
            else: page = urllib.request.urlopen(filename).read()
            return page
        except FileExistsError: print('File not Found')

    ############################################################################
    ##----------------------- End supporting functions -----------------------##
    ############################################################################

    '''-------------------------------------------------------------------------
    ##------------------ Functions to get details from file ------------------##
    -------------------------------------------------------------------------'''

    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Get List from csv
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def get_csv(self, filename):
        try:
            with open ('Test_Files/'+filename+'.csv', newline='') as csvF:
                table = csv.reader(csvF)
                tmp = []
                for row in table:
                    tmp.append(row)
                self.table = tmp
        except FileNotFoundError:
            print('That please recheck the file, all files in Test_Files folder')


    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Get List from html or eml
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''


    def get_html(self, filename):
        try:
            page = self.file_check(filename)
            soup = bs(page,'html.parser')
            tables =  soup.find_all('table')
            tbls = []
            # Record all tables in the program to pick one from it
            for table in tables:
                tbl = [] #
                #find the table rows
                trs = table.findChildren('tr')
                ths = trs[0].findChildren('th')
                row = []
                #get the header information if its stored as header
                for th in ths:
                    row.append(th.text)
                if row != []: tbl.append(row)

                for tr in trs:
                    #find the cells
                    tds = tr.findChildren('td')
                    row = []
                    for td in tds:
                        # Now get cell data
                        row.append(td.text.replace('\n',''))
                    #row = row[]
                    if row != []:
                        tbl.append(row)
                if tbl != []:
                    tbls.append(tbl)

            if len(tbls) == 1:
                self.table = tbls[0]
                #for i in tbls[0]:
            elif len(tbls) > 1:
                # pick and update table from choices of table
                self.pick_table(tbls)
            else:
                print('There are no Tables in this page')

        # ----- Problems in reading files or url information --------#
        except FileNotFoundError:
            print('That please recheck the file, all files in Test_Files folder')
        except urllib.error.URLError:
            print('File or link does not exist')
        except ValueError:
            print('File or link does not exist')


    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Get List from ics
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def get_ics(self, filename):
        try:
            with open('../Test_Files/'+filename+'.ics','rb') as icsF:
                cal = Calendar.from_ical(icsF.read())
                #csvF = open('../New_Files/' +filename + '.csv', 'w')
                rows = [['SUMMARY','DTSTART','DTEND','NOTES','LOCATION']]
                for component in cal.walk():
                    if component.name == "VEVENT":
                        row = []
                        #f =
                        row.append(str(component.get('summary')))
                        # Extract and format the date accordingly
                        start = vDatetime.from_ical(component.get('dtstart').to_ical().decode())
                        row.append(str(start.strftime('%m-%d-%Y %I:%M %p')))
                        end = vDatetime.from_ical(component.get('dtend').to_ical().decode())
                        row.append(str(end.strftime('%m-%d-%Y %I:%M %p')))

                        row.append(str(component.get('description')))
                        row.append(str(component.get('location')))
                        #make sure any data types are covered
                        for i in range(len(row)):
                            if row[i] == 'None' or row[i] == None:
                                row[i] = ''
                            #else:
                            #    row[i] = '"'+row[i]+'"'
                        #print (row)
                        rows.append(row)
                self.table = rows
        except FileNotFoundError:
            print('File does not exist')

    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Get List from Tex
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def get_tex(self, filename):
        from TexSoup import TexSoup
        try:
            # Get the file
            texfile = open('../Test_Files/'+filename+'.tex')
            doc = texfile.read().replace('%','')
            texfile.close()
            ts = TexSoup(doc)
            #Find the table
            table = ts.find('tabular')
            table.args.clear()
            # remove all unneccesary things and remove them
            while table.hline != None: table.hline.delete()
            while table.rowcolor != None: table.rowcolor.delete()
            while table.cellcolor != None: table.cellcolor.delete()

            # remove multirows and multicolumns replace with value
            while table.find('multicolumn') != None: table.replace(table.multicolumn, [i for i in table.multicolumn][-1])
            while table.find('multirow') != None:table.replace(table.multirow, [i for i in table.multirow][-1])

            #clean to match class table clearing unnecessary symbols
            newTable = []
            for i in table:
                newTable.append(str(i).replace(' \n','').replace('\n',''))
            table = "".join(newTable).split("\\\\")

            #split up the rows into cells
            for j in table:
                x = table.index(j)
                j = j.replace(' & ','&').replace(' &','&').replace('& ','&').replace('{','').replace('}','')
                table[x] = j.split('&')
            if table[-1] == ['']: table.pop(-1)
            self.table = table

        except FileNotFoundError:
            print('file does not exist')
    ############################################################################
    ##-------------- End Functions to get details from file ------------------##
    ############################################################################

    '''-------------------------------------------------------------------------
    ##------------------ Functions to get details from file ------------------##
    -------------------------------------------------------------------------'''

    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Make an html file from the List [table]
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def mk_html(self, filename):
        htf = open('../New_Files/'+filename+'.html', 'w+')
        htf.write(self.html_data())
        htf.close()

    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Make an Eml file from the List [table]
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def mk_eml(self, filename):
        from email import generator
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        ## Get the header information
        mail = MIMEMultipart('alternative')
        mail['Subject'] = 'A Test of file conversion'
        mail['From'] = filename+'@email.com'
        mail['To'] = 'Test@email.com'
        ## Create the body of the email
        body = MIMEText(self.html_data(), 'html')
        mail.attach(body)
        ## Save the file
        with open("../New_Files/"+filename+'.eml', 'w+') as eml_file:
            out = generator.Generator(eml_file)
            out.flatten(mail)

    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Make a csv file from the List [table]
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def mk_csv(self, filename):
        f = open('../New_Files/'+filename+".csv", 'w+')
        for row in self.table:
            f.write('"'+'","'.join(row)+'"\n')
        f.close()

    ''' """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" ***
        Make a Tex file from the List [table]
    *** """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" '''
    def mk_tex(self, filename):
        # create he latex doc
        doc = Document()
        # Check to avoid index error and create the table border lines
        if self.table != []:
            size = len(self.table[0])
            header = '|l'* size
            header += '|'
        else:
            print('No values assigned to the table')
            return None

        # Fill the table and create a tex file in the New_Files Folder
        with doc.create(Tabular(header)) as table:
            table.add_hline()
            for row in self.table:
                table.add_row(row)
                print(row)
                table.add_hline()
        doc.generate_tex('../New_Files/'+filename)
        #/* doc.generate_pdf() #: Needs latex compiler to work

if __name__ == "__main__":
    link=('http://www.genevievedupuis.com/BloodBowl/WeatherTable.php')
    ft = Transformer()
    name ='test'
    '''
    ft.get_csv(name+"_csv")
    print(30*'#',name+"_csv", '*'*30 )
    print(ft.table,'\n')

    ft.get_html(name+"_eml")
    print(30*'#',name+"_eml", '*'*30 )
    print(ft.table,'\n')

    ft.get_tex(name+"_tex")
    print(30*'#',name+"_tex", '*'*30 )
    print(ft.table,'\n')
    '#''
    ft.get_ics(name+"_ics")
    print(30*'#',name+"_ics", '*'*30 )
    print(ft.table,'\n')
    '''
    ft.get_html(name+"_html")
    print(30*'#',name+"_html", '*'*30 )
    print(ft.table,'\n')
    #'''