import glob
import csv
from datetime import datetime, timedelta


def read_csv2dict(fname):
    data = []
    with open(fname, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:

            #skip header
            if line_count == 0:
                #print("----------")
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

                #zero duration stamps do not have ending times
                #print(row['Start time'], row['End time'], row['Duration'])
                if row['End time'] == '':
                    continue
                tend   = datetime.strptime(row['End time'],   '%H:%M:%S')

                #-------------------
                #clean special weeks when toggl clock was off from HEL-NYC move
                if datetime.strptime('Jan 6 2020 1:00AM', '%b %d %Y %I:%M%p') < day < datetime.strptime('Jan 19 2020 6:00AM', '%b %d %Y %I:%M%p'):
                    d0 = day + timedelta(hours=tstart.hour, minutes=tstart.minute, seconds=tstart.second)
                    d1 = day + timedelta(hours=tend.hour, minutes=tend.minute, seconds=tend.second)

                    dshift0 = d0 - timedelta(hours=7)
                    dshift1 = d1 - timedelta(hours=7)
                    print("shifting:", dshift0, dshift1)

                    tstart = tstart.replace(hour=dshift0.hour, minute=dshift0.minute, second=dshift0.second)
                    tend = tend.replace(hour=dshift1.hour, minute=dshift1.minute, second=dshift1.second)

                    day = dshift0
                    

                #-------------------
                tlenP   = datetime.strptime(row['Duration'],   '%H:%M:%S')
                tlen = 3600.0*tlenP.hour + 60.0*tlenP.minute + tlenP.second

                d = {
                    'project':     row['Project'],
                    'description': row['Description'],
                    'day':         day,
                    'start':       tstart,
                    'end':         tend,
                    'duration':    tlen,
                    }

                #remove summary line
                if d['project'] == '':
                    continue

                data.append(d)
            line_count += 1
    return data



#--------------------------------------------------

def read_toggl_reports():

    datadir = '/Users/natj/Dropbox/toggl-reports/'
    
    # get report csv files
    reports = []
    for f in glob.glob(datadir+'*.csv'):
        reports.append(f)
    
    print(reports)

    ds = []
    for report in reports:
        d = read_csv2dict(report)

        for dicts in d:
            ds.append(dicts)

    return ds


