import win32evtlog# requires pywin32 pre-installed
import datetime, time
from datetime import datetime
import logging

logging.basicConfig(filename="OperatingSystem.log", level=logging.DEBUG,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

def fun():
    server = 'localhost' # name of the target computer to get event logs
    logtype = 'System' # 'Application' # 'Security'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    #total = win32evtlog.GetNumberOfEventLogRecords(hand)
    hand = win32evtlog.OpenEventLog(server,logtype)

    begin_sec = time.time()
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin_sec))
    print(begin_sec)

    time.sleep(30)

    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            #print(event.TimeGenerated)
            datetime_object = datetime.strptime(str(event.TimeGenerated), '%Y-%m-%d %H:%M:%S')
            seconds = time.mktime(datetime_object.timetuple())

            if(begin_sec<=seconds):
                #print(begin_sec)
                #print(seconds)
                print('Time Generated:', event.TimeGenerated)
                print('Source Name:', event.SourceName)
                print('Event Type:', event.EventType)
                print('String inserts', event.StringInserts)
                writeLog(event.EventType, event.TimeGenerated, event.SourceName)


def writeLog(type,date,name):
    typeStr = getType(type)
    print(type)
    print(date)
    print(name)

    #TO DO


    #logging.info(data[1], extra={"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":"tinyproxy[9456]"})

def getType(a):
    if(a==2):
        return "Warning"
    elif(a==4):
        return "Information"
    else:
        return "Undefined"


def fun1():
    while True:
        fun()

fun1()