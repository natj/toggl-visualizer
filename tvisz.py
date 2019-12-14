import glob
import csv
from datetime import datetime


def read_csv2dict(fname):
    data = []
    with open(fname, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:

            #skip header
            if line_count == 0:
                print("----------")
                #print(row)
                line_count += 1
            else:

                #example row for what we parse
                #------------------------------------
                #End date: '2019-12-08', 
                #Task: ' ', 
                #Description: ' ', 
                #Tags: '', 
                #Start time: '17:37:59', 
                #Project: 'organize/reflect', 
                #End time: '18:03:23', 
                #Client: '', 
                #Amount (): '', 
                #Billable: 'No', 
                #Duration: '00:25:24', 
                #Start date: '2019-12-08', 
                #\xef\xbb\xbfUser: 'Nattila Joonas', 
                #Email: 'nattila.joonas@gmail.com'

                #parse day
                #datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                day = datetime.strptime(row['Start date'], '%Y-%m-%d')

                #parse times
                tstart = datetime.strptime(row['Start time'], '%H:%M:%S')
                tend   = datetime.strptime(row['End time'],   '%H:%M:%S')
                tlen   = datetime.strptime(row['Duration'],   '%H:%M:%S')

                d = {
                    'project':     row['Project'],
                    'description': row['Description'],
                    'day':         day,
                    'start':       tstart,
                    'end':         tend,
                    'duration':    tlen,
                    }

                data.append(d)
            line_count += 1
    return data



#--------------------------------------------------


#--------------------------------------------------

datadir = '/Users/natj/Dropbox/toggl-reports/'

# get report csv files
reports = []
for f in glob.glob(datadir+'*.csv'):
    reports.append(f)

print(reports)
for report in reports:
    d = read_csv2dict(report)

    print(d)


