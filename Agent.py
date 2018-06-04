import numpy as np
import requests
import urllib
import ssl
import socket
import win32evtlog# requires pywin32 pre-installed
import datetime, time
from datetime import datetime
import logging
import platform

logging.basicConfig(filename="OperatingSystem.log", level=logging.DEBUG,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

class Log:

    def __init__(self, type , description, date, ip,
                 host, facility, tag):
        self.type = type
        self.description = description
        self.date = date
        self.ip = ip
        self.tag = tag
        self.host = host
        self.facility = facility


    def make_string(self):
        return str(self.type) + "#" + str(self.description) + "#" + str(self.date)

class Agent:

    def __init__(self,property_file = "scripts/Agents/config.properties"):
        self.property_file = property_file

    def send_post_request(self, log):
        request_url = "https://localhost:8443/agent/saveLog";
        data= {}
        data['type'] = log.type.strip()
        data['description'] = log.description.strip()
        data['date'] = str(log.date).strip()
        data['ip'] = log.ip.strip()
        data['host'] = log.host.strip()
        data['facility'] = log.ip.strip()
        data['tag'] = log.tag.strip()
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_verify_locations(capath='C:/Users/milan/Desktop/Salic/Bezbjednost/BS')
        d = urllib.parse.urlencode(data).encode("UTF-8")
        urllib.request.urlopen(request_url, data=d, context=context)

    def send(self, file_name, types, last_lines):
        logFile = open(file_name)
        lines = logFile.readlines()
        logFile.close()
        if len(lines) == last_lines:
            print("Nothing to send.")
        else:
            index = last_lines
            while index < len(lines) :
                line = lines[index]
                elements = line.split("|")
                print(elements[5])
                if elements[5] in types:
                    datetime_object = datetime.strptime(elements[1][:19], "%Y-%m-%d %H:%M:%S")
                    l = Log(elements[5],elements[7],datetime_object,socket.gethostbyname(socket.gethostname()),elements[3]
                            ,elements[4],elements[6])
                    self.send_post_request(l)
                else:
                    print("Not sending.")
                index = index + 1
        return len(lines)








def fun():
    server = 'localhost' # name of the target computer to get event logs
    logtype = 'System' # 'Application' # 'Security'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    #total = win32evtlog.GetNumberOfEventLogRecords(hand)
    hand = win32evtlog.OpenEventLog(server,logtype)

    begin_sec = time.time()
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin_sec))

    time.sleep(30)

    events = win32evtlog.ReadEventLog(hand, flags,0)
    if events:
        for event in events:
            datetime_object = datetime.strptime(str(event.TimeGenerated), '%Y-%m-%d %H:%M:%S')
            seconds = time.mktime(datetime_object.timetuple())

            if(begin_sec<=seconds):
                writeLog(event.EventType, event.TimeGenerated, event.SourceName)


def writeLog(type,date,name):
    request_url = "https://localhost:8443/agent/saveLog";
    data = {}
    data['type'] = getType(type).strip()
    data['description'] = name.strip()
    data['date'] = str(date).strip()
    data['ip'] = socket.gethostbyname(socket.gethostname())
    data['host'] = socket.gethostname().strip()
    data['facility'] = "tinyproxy[9456]".strip()
    data['tag'] = "daemon".strip()
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(capath='C:/Users/milan/Desktop/Salic/Bezbjednost/BS')
    d = urllib.parse.urlencode(data).encode("UTF-8")
    urllib.request.urlopen(request_url, data=d, context=context)

def getType(a):
    if(a==2):
        return "WARNING"
    elif(a==4):
        return "INFO"
    elif(a==3):
        return "CRITICAL"
    else:
        return "ERROR"



if __name__ == '__main__':
    separator = "="
    keys = {}

    with open('config.properties') as f:

        for line in f:
            if separator in line:

                # Find the name and value by splitting the string
                name, value = line.split(separator, 1)

                # Assign key value pair to dict
                # strip() removes white space from the ends of strings
                keys[name.strip()] = value.strip()

    types = keys['types'].split(',')
    files = keys['filePaths'].split(',')
    last_lines = np.zeros(len(files), dtype=object)
    a = Agent()
    while True:
        i = 0
        for file in files:
            last_lines[i] = a.send(file, types, last_lines[i])
            i = i + 1
        if platform.system() == "Windows":
            fun()
        else:
            print("System is Linux")
        time.sleep(10)