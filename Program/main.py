#from bs4 import BeautifulSoup
import csv
import arrow
import ics

### Convert any csv meeting a format to ics
def csv2ics(filename):
  try:
    with open(filename+'.csv', newline='') as csvF:
      table = csv.DictReader(csvF) #use a dict to easily find specific headers
      cal = ics.Calendar()
      for row in table:
        # create a new calendar Event and fill it
        ev = ics.Event()
        #-# Get the different attributes necessary for an event in the Calendar #-#
        if row['SUMMARY'] != None:
          ev.name = row['SUMMARY']
        else:
          ev.name = ''
        
        # No calender event is complete without start and end date 
        if row['DTSTART'] != None and row['DTEND'] != None:
          form = 'MM-DD-YYYY hh:mm a' #Format
          ev.begin = arrow.get(row['DTSTART'],form)
          ev.end = arrow.get(row['DTEND'],form)
        else:
          raise Exception('Must Have both start and end dates')
        try:
          if row['NOTES'] != None:
            ev.description = row['NOTES']
          elif row['DESCRIPTION'] != None:
            ev.description = row['DESCRIPTION']
        finally:
          if row['LOCATION'] != None:
            ev.location = row['LOCATION']
        
        #Now save the event in the Calendar
        cal.events.add(ev)
      # After the 
      f = open(filename+'.ics', 'w')
      f.writelines(cal)
      f.close()
  # Error Handling options
  except FileNotFoundError:
    print("This file does not exist",filename)
  except KeyError:
    print('Check that the file head structure follows:\n',
          'SUMMARY, DTSTART, DTEND, NOTES, LOCATION')


#from ics import Calendar as Cal

from icalendar import Calendar, Event

def ics2csv(filename):
  with open('test.ics','rb') as g:
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
      if component.name == "VEVENT":
        print("---------------------------------")
        print(component.get('summary'))
        print(component.get('dtstart').to_ical().decode())
        print(component.get('dtend').to_ical().decode())
        print(component.get('note'))
  #g.close()

if __name__ == "__main__":
  # execute only if run as a script
  #csv2ics('test')
  ics2csv('test')
  

  '''
  with open('test.ics', 'rb') as f:
    filed = f.read()
    c = Calendar(filed)
    print(c)
  #print(requests.get(url).text)
  #print(c.events)
  #
  g = open('file.ics','rb')
  gcal = Calendar.from_ical(g.read())
  for component in gcal.walk():
    if component.name == "VEVENT":
      print "---------------------------------"
      print component.get('summary')
      print component.get('dtstart').to_ical()
      print component.get('dtend').to_ical()
  g.close()

#'
strTable = 
['<html>',
'  <table>',
'    <tr>',
'      <th>Char</th>',
'      <th>ASCII</th>',
'    </tr>',
'  </table>',
'</html>']
#soup = BeautifulSoup('', 'html.parser')

for num in range(33,48):
 symb = chr(num)
 strRW = "<tr><td>"+str(symb)+ "</td><td>"+str(num)+"</td></tr>"
 strTable = strTable+strRW
 
strTable = strTable+"</table></html>"
 
hs = open("asciiCharHTMLTable.html", 'w')
hs.write(strTable)
hs.close()
 
print (strTable)
'''