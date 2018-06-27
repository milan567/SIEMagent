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
    #ovdje mora da se salje Firewallu.

def getType(a):
    if(a==2):
        return "WARNING"
    elif(a==4):
        return "INFO"
    elif(a==3):
        return "CRITICAL"
    else:
        return "ERROR"


def send_log_to_siem_center(line):
    elements = line.split("|")
    print(elements[5])
    datetime_object = datetime.strptime(elements[1][:19], "%Y-%m-%d %H:%M:%S")
    request_url = "https://localhost:8443/agent/saveLog";
    data = {}
    data['type'] = elements[5]
    data['description'] = elements[7]
    data['date'] = str(datetime_object).strip()
    data['ip'] = socket.gethostbyname(socket.gethostname())
    data['host'] = elements[3]
    data['facility'] = elements[4]
    data['tag'] = elements[6]
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(capath='C:/Users/milan/Desktop/Salic/Bezbjednost/BS')
    d = urllib.parse.urlencode(data).encode("UTF-8")
    urllib.request.urlopen(request_url, data=d, context=context)




def receive_and_send_messages(conn_obj,addr):
    print("Got a connection from ", addr)
    print("Recieve and send messages")
    print(conn_obj)
    msg_from_client = conn_obj.recv(2048)
    if not msg_from_client:
        print("<...No Relpy...> ")
    else:
        message = msg_from_client.decode("utf-8")
        print(message)
        print("Message successfully recieved")
        send_log_to_siem_center(message)


def send_post_messages(log,sock):
    print("Sending messages to firewall")
    msg_for_server = bytes(log, 'utf-8')
    sock.send(msg_for_server)




def send_logs_to_firewall(file_name, types, last_lines,sock):
    print("Sending logs to firewall")
    logFile = open(file_name)
    lines = logFile.readlines()
    logFile.close()
    if len(lines) == last_lines:
        print("Nothing to send.")
    else:
        index = last_lines
        while index < len(lines):
            line = lines[index]
            elements = line.split("|")
            print(elements[5])
            if elements[5] in types:
                datetime_object = datetime.strptime(elements[1][:19], "%Y-%m-%d %H:%M:%S")
                l = Log(elements[5], elements[7], datetime_object, socket.gethostbyname(socket.gethostname()),
                        elements[3]
                        , elements[4], elements[6])
                send_post_messages(line,sock)
            else:
                print("Not sending.")
            index = index + 1
    return len(lines)



def send_data_to_siem_center(keys):
    request_url = "https://localhost:8443/agent/sendAgentData";
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    d = urllib.parse.urlencode(keys).encode("UTF-8")
    urllib.request.urlopen(request_url, data=d, context=context)


def make_client_connection(port_number):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_name = socket.gethostname()  # To get the name of host
    print("The name of local machine", host_name)
    host_port_pair = (host_name, port_number)  # A tuple

    sock.connect(host_port_pair)
    return sock


def make_server_connection(port_number):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_name = socket.gethostname()  # To get the name of host

    host_port_pair = (host_name, port_number)  # A tuple
    print(host_port_pair)
    sock.bind(host_port_pair)  # Bind address to the socket

    sock.listen(10)
    conn_obj, addr = sock.accept()
    print("Port connection made.")
    return  (conn_obj ,addr)


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
    enabled = keys['enabled']
    role = keys['role']
    ports = keys['ports']
    port = keys['port']
    last_lines = np.zeros(len(files), dtype=object)
    batch = keys['batch']
    send_data_to_siem_center(keys)
    a = Agent()
    sock = []
    addr = []
    if role != "FIREWALL":
        print("Making socket for os")
        sock = make_client_connection(eval(port))
    else:
        print("Making socket for firewall")
        port_for_server = ports.split(",")
        for p in port_for_server:
            ad, bd = make_server_connection(eval(p))
            sock.append(ad)
            addr.append(bd)
    while True:
        i = 0
        if role == "FIREWALL":
            for file in files:
                print("reading firewall files and send to server.")
                last_lines[i] = a.send(file, types, last_lines[i])
                i = i + 1
            for j in range(0,len(sock)):
                receive_and_send_messages(sock[j],addr[j])
        else:
            if enabled == "TRUE":
                if platform.system() == "Windows":
                    print("Reading os logs - OS")
                    fun()
                else:
                    print("System is Linux")
            for file in files:
                send_logs_to_firewall(file,types, last_lines[i],sock)
                i = i + 1
        time.sleep(batch)