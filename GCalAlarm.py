#!/usr/bin/python -W ignore::DeprecationWarning

# if true we run arduino light show 
useArd = True;
ardDev = '/dev/ttyUSB0'

try:
  from xml.etree import ElementTree # for Python 2.5 users
except ImportError:
  from elementtree import ElementTree
import datetime
from datetime import datetime, timedelta, date, time
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time
import urllib
import os

import signal
def signal_handler(signal, frame):
    if( useArd ):
        ard.writeLine('O')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if( useArd ):
    from arduino import *
    try:
        ard = arduino(ardDev)
    except:
        print 'Failed to open Arduino'
        sys.exit(0);

def main():
    if( len(sys.argv) < 2 ):
        print 'Usage: ',sys.argv[0],' publicCalendarID';
        sys.exit(0);

    calID = '%s@group.calendar.google.com' % sys.argv[1];

    calendar_service = gdata.calendar.service.CalendarService()
    
    query = gdata.calendar.service.CalendarEventQuery(
            calID,
            'public',
            'full')
    
    time_now  = datetime.now()
    time_then = time_now + timedelta(days=7)
    query.start_min = time_now.isoformat()
    query.start_max = time_then.isoformat()

    query.orderby = 'starttime';
    query.sortorder = 'a';
    
    feed = calendar_service.CalendarQuery(query)
    
    if( len(feed.entry) == 0 ):
        print 'Sorry, no alarms found'
        sys.exit(0)
    
    # if an_event is recurring then it
    # will have a bunch of unordered 'when's
    # we want the earliest one...

    minTime = feed.entry[0].when[0].start_time

    for an_event in feed.entry:
        for a_when in an_event.when:
            if a_when.start_time < minTime:
                minTime = a_when.start_time

    
    print 'Alarm: %s' % (an_event.title.text,)
    alarm_time = minTime;
    
    isoformat = '%Y-%m-%dT%H:%M:%S.%fZ' 
    datetime_alarm = datetime.strptime( alarm_time, isoformat )
    
    printformat = '%H:%M:%S on %b %d'
    print '\t%s' % datetime_alarm.strftime(printformat)
    print
    print
    
    while 1:
        now = datetime.now()
    
        if( now > datetime_alarm ):
            print
            print 'Alarm!!! ALARM!!!'
            print
        
            cmd='mpc play'
            os.system(cmd)
            
            if( useArd ):
                # turn lights on and off
                while 1:
                    ard.writeLine('G')
                    ard.writeLine('R')
    
            sys.exit(0)
    
        print 'Still too early... ', now.strftime(printformat), ' (', datetime_alarm.strftime(printformat), ')'
        time.sleep(1)

if __name__ == "__main__":
    main();

