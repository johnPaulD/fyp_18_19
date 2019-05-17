import csv
import
from bs4 import BeautifulSoup as bs
##--------------------------------- CSV to HTML ---------------------------##
def csv2html(filename):
    try:
        with open ('../Test_Files/'+filename+'.csv', newline='') as csvF:
            htf = open('../New_Files/htf.html', 'w')
            table = csv.reader(csvF)
            beg = '<!-DOCTYPE html>\n<html>\n\t<style>table, th, td { border: 1px solid black; border-collapse: collapse; }</style>\n\t<body>\n\t\t<table>\n'
            end = '\t\t</table>\n\t</body>\n<\html>'
            htf.write(beg)
            th = ""
            for row in table:
                htf.write('\t\t\t<tr>\n')
                if th == "":
                    th = '1'
                    for col in row:
                        htf.write('\t\t\t\t<th>'+col+'</th>\n')
                else:
                    for col in row:
                        htf.write('\t\t\t\t<td>'+col+'</td>\n')
                htf.write('\t\t\t</tr>\n')
            htf.write(end)
            htf.close()
    except FileNotFoundError:
        print('That please recheck the file, all files in Test_Files folder')

from bs4 import BeautifulSoup as bs
import urllib.request
from time import sleep
from pathlib import Path

def html2Array(source):
    try:
        f = Path(source+".html")
        page = ""
        if f.is_file():
            with open(source+'.html') as nf:
                page = nf.read()
        else:# Will throw file and url not found message if link fails
            page = urllib.request.urlopen(source).read()
            #page = requests.get(source).text
        soup = bs(page,'html.parser')
        tables =  soup.find_all('table')
        tbls = []

        for table in tables:
            tbl = [] #
            #find the table rows
            trs = table.findChildren('tr')
            for tr in trs:
                #find the cells
                tds = tr.findChildren('td')
                row = []
                for td in tds:
                    # Now get cell data
                    row.append(td.text)
                #row = row[]
                if row != []:
                    tbl.append(",".join(row))
            if tbl != []:
                tbls.append(tbl)
        if tbls == []:
            return None
        return tbls
    except FileNotFoundError:
        print('That please recheck the file, all files in Test_Files folder')
    except urllib.error.URLError:
        print('File or link does not exist')
    except ValueError:
        print('File or link does not exist')


def html2csv(name):
    # Set the right name for a and let urls pass
    f = Path(name+'.html')
    cv = ""
    if f.is_file():
        cv = name+'.csv'
    else:
        cv = "ninpou.csv"
    tables = html2Array(name)

    if tables == None: print('Do Nothing')
    elif len(tables) == 1:
        f = open(cv, 'w+')
        for i in tables[0]:
            f.write(i+'\n')
            print(i)
        f.close
        #f = open(cv).read()
        #print(f)
        print('** Successfully Created',cv,' **')
    else:
        print("*"*80,"\nFrom below pick the table you want")
        i = 1
        for t in tables:
            print('[',i,']\t', t)
            i += 1

if __name__ == "__main__":
    html2csv('http://www.genevievedupuis.com/BloodBowl/WeatherTable.php')
    csv2html('../Test_Files/test')
