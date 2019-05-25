#from bs4 import BeautifulSoup
import csv
import arrow
import ics

### Convert any csv meeting a format to ics
def csv2ics(filename):
    try:
        with open('../Test_Files/' +filename+'.csv', newline='') as csvF:
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
                if row['NOTES'] != None:
                    ev.description = row['NOTES']
                elif row['DESCRIPTION'] != None:
                    ev.description = row['DESCRIPTION']

                if row['LOCATION'] != None:
                    ev.location = row['LOCATION']

                #Now save the event in the Calendar
                cal.events.add(ev)
            # create and save the ics file
            f = open('../New_Files/' +filename+'.ics', 'w')
            f.writelines(cal)
            f.close()
            print("Succesfully Created",'../New_Files/' + filename + '.ics')
          #Error Handling options
    except FileNotFoundError:
        print("This file does not exist",filename)
    except KeyError:
        print('Check that the file head structure follows:\n',
              'SUMMARY,DTSTART,DTEND,NOTES,LOCATION')


#from ics import Calendar as Cal

from icalendar import Calendar, vDatetime
def ics2csv(filename):
    try:
        with open('../Test_Files/' +filename+'.ics','rb') as g:
            gcal = Calendar.from_ical(g.read())
            csvF = open('../New_Files/' +filename + '.csv', 'w')
            lines = ['SUMMARY,DTSTART,DTEND,NOTES,LOCATION']
            for component in gcal.walk():
                if component.name == "VEVENT":
                    line = []
                    #f =
                    line.append(component.get('summary'))
                    # Extract and format the date accordingly
                    st = vDatetime.from_ical(component.get('dtstart').to_ical().decode())
                    line.append(st.strftime('%m-%d-%Y %I:%M %p'))
                    en = vDatetime.from_ical(component.get('dtend').to_ical().decode())
                    line.append(en.strftime('%m-%d-%Y %I:%M %p'))

                    line.append(component.get('description'))
                    line.append(component.get('location'))
                    #make sure any data types are covered
                    for i in range(len(line)):
                        if line[i] == None:
                            line[i] = ''
                        else:
                            line[i] = '"'+line[i]+'"'
                    #print (line)
                    lines.append(",".join(line))
            csvF.writelines("\n".join(lines))
            csvF.close()
            print("Succesfully Created",'../New_Files/' + filename + '.csv')
    except FileNotFoundError:
        print("This file does not exist",filename)



if __name__ == "__main__":
  # execute only if run as a script
  ics2csv('test')
  csv2ics('test')
