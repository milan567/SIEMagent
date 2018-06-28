import json

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
import websocket
import sys
import time
import threading


logging.basicConfig(filename="OperatingSystem.log", level=logging.DEBUG,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")


class AgentData:
    def __init__(self,name,filePaths,types,enabled,role,ports,port,batch,level):
        self.name = name
        self.filePaths = filePaths
        self.types = types
        self.enabled = enabled
        self.role = role
        self.ports = ports
        self.port = port
        self.batch = batch
        self.level = level


class Log:

    def __init__(self, type , description, date, ip,
                 host, facility, tag, agent_name):
        self.type = type
        self.description = description
        self.date = date
        self.ip = ip
        self.tag = tag
        self.host = host
        self.facility = facility
        self.agent_name = agent_name


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
        data['name'] = log.agent_name
        print(data)
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_verify_locations(capath='C:/Users/milan/Desktop/Salic/Bezbjednost/BS')
        d = urllib.parse.urlencode(data).encode("UTF-8")
        ad = urllib.request.urlopen(request_url, data=d, context=context)
        string = ad.read().decode('utf-8')
        json_obj = json.loads(string)
        return json_obj

    def send(self, file_name, types, last_lines,agent_name):
        print("AGENT NAME")
        print(agent_name)
        print("AGENT NAME")
        logFile = open(file_name)
        lines = logFile.readlines()
        logFile.close()
        ad = None
        if len(lines) == last_lines:
            print("Nothing to send.")
        else:
            index = last_lines
            while index < len(lines) :
                line = lines[index]
                elements = line.split("|")
                print(elements[5])
                print(agent_name)
                if elements[5] in types:
                    datetime_object = datetime.strptime(elements[1][:19], "%Y-%m-%d %H:%M:%S")
                    l = Log(elements[5],elements[7],datetime_object,socket.gethostbyname(socket.gethostname()),elements[3]
                            ,elements[4],elements[6],agent_name)
                    ad = self.send_post_request(l)
                else:
                    print("Not sending.")
                index = index + 1
        print(ad)
        print("AGENT DATA IN SEND")
        return len(lines), ad








def fun(agent_name):
    server = 'localhost' # name of the target computer to get event logs
    logtype = 'System' # 'Application' # 'Security'
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    #total = win32evtlog.GetNumberOfEventLogRecords(hand)
    hand = win32evtlog.OpenEventLog(server,logtype)

    begin_sec = time.time()
    begin_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(begin_sec))

    time.sleep(30)

    events = win32evtlog.ReadEventLog(hand, flags,0)
    json_object = None
    if events:
        for event in events:
            datetime_object = datetime.strptime(str(event.TimeGenerated), '%Y-%m-%d %H:%M:%S')
            seconds = time.mktime(datetime_object.timetuple())

            if(begin_sec<=seconds):
                json_object = writeLog(event.EventType, event.TimeGenerated, event.SourceName,agent_name)
    return json_object

def writeLog(type,date,name,agent_name):
    request_url = "https://localhost:8443/agent/saveLog";
    data = {}
    data['type'] = getType(type).strip()
    data['description'] = name.strip()
    data['date'] = str(date).strip()
    data['ip'] = socket.gethostbyname(socket.gethostname())
    data['host'] = socket.gethostname().strip()
    data['facility'] = "tinyproxy[9456]".strip()
    data['tag'] = "daemon".strip()
    data['name'] = agent_name
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(capath='C:/Users/milan/Desktop/Salic/Bezbjednost/BS')
    d = urllib.parse.urlencode(data).encode("UTF-8")
    ad = urllib.request.urlopen(request_url, data=d, context=context)
    print("Poziv 1")
    string = ad.read().decode('utf-8')
    json_obj = json.loads(string)
    return json_obj


def getType(a):
    if(a==2):
        return "WARNING"
    elif(a==4):
        return "INFO"
    elif(a==3):
        return "CRITICAL"
    else:
        return "ERROR"


def send_log_to_siem_center(line,agent_name):
    elements = line.split("|")
    print(elements[5])
    datetime_object = datetime.strptime(elements[1][:19], "%Y-%m-%d %H:%M:%S")
    request_url = "https://localhost:8443/agent/saveLog";
    data = {}
    print("Prikaz!!!")
    print(line)
    data['type'] = elements[5]
    data['description'] = elements[7]
    data['date'] = str(datetime_object).strip()
    data['ip'] = socket.gethostbyname(socket.gethostname())
    data['host'] = elements[3]
    data['facility'] = elements[4]
    data['tag'] = elements[6]
    data['name'] = elements[8]
    print(elements[7])
    print("ime agenta")
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_verify_locations(capath='C:/Users/milan/Desktop/Salic/Bezbjednost/BS')
    d = urllib.parse.urlencode(data).encode("UTF-8")
    ad = urllib.request.urlopen(request_url, data=d, context=context)
    print("Poziv 2")
    string = ad.read().decode('utf-8')
    return string



def receive_and_send_messages(conn_obj,addr,agent_name):
    print("Got a connection from ", addr)
    print("Recieve and send messages")
    print(conn_obj)
    msg_from_client = conn_obj.recv(2048)
    if not msg_from_client:
        print("<...No Relpy...> ")
        return None
    else:
        message = msg_from_client.decode("utf-8")
        print(message)
        print("Message successfully recieved")
        agent_data = send_log_to_siem_center(message,agent_name)
        msg_for_client = bytes(agent_data, 'utf-8')
        print("Trying to send message")
        conn_obj.send(msg_for_client)
        print("Message is sent from firewall")
        print(agent_data)


def send_post_messages(log,sock):
    print("Sending messages to firewall")
    msg_for_server = bytes(log, 'utf-8')
    sock.send(msg_for_server)
    msg_from_server = sock.recv(2048)
    print(msg_from_server)
    print("Message received!")
    json_obj = json.loads(msg_from_server)
    return json_obj




def send_logs_to_firewall(file_name, types, last_lines,sock,agent_name):
    agent_data = None
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
                        , elements[4], elements[6],agent_name)
                print(line)
                print("bla bla bla")
                string = (line.strip()) + "|" + agent_name
                print(string)
                agent_data = send_post_messages(string,sock)
            else:
                print("Not sending.")
            index = index + 1
    return len(lines) , agent_data



def send_data_to_siem_center(keys):
    request_url = "https://localhost:8443/agent/sendAgentData"
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    d = urllib.parse.urlencode(keys).encode("UTF-8")
    ad =urllib.request.urlopen(request_url, data=d, context=context)

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
    agentData = AgentData(keys['name'],keys['filePaths'].split(','),keys['types'].split(','),keys['enabled'],
                        keys['role'],keys['ports'],keys['port'],keys['batch'],keys['level'])
    last_lines = np.zeros(len(agentData.filePaths), dtype=object)
    send_data_to_siem_center(keys)
    a = Agent()
    sock = []
    addr = []
    if agentData.role != "FIREWALL":
        print("Making socket for os")
        sock = make_client_connection(eval(agentData.port))
    else:
        print("Making socket for firewall")
        port_for_server = agentData.ports.split(",")
        for p in port_for_server:
            ad, bd = make_server_connection(eval(p))
            sock.append(ad)
            addr.append(bd)
    json_object = None
    while True:
        i = 0
        print("AGENT DATA")
        print(agentData.role)
        if agentData.role == "FIREWALL":
            print("Usao")
            for file in agentData.filePaths:
                print("reading firewall files and send to server.")
                last_lines[i], json_object = a.send(file, agentData.types, last_lines[i],agentData.name)
                if json_object != None:
                    #agentData.name = json_object['name']
                    agentData.filePaths = json_object['filePaths']
                    agentData.level = json_object['level']
                    agentData.batch = json_object['batch']
                    agentData.port = json_object['port']
                    agentData.ports = json_object['ports']
                    agentData.enabled = json_object['enabled']
                    agentData.role = json_object['role']
                    agentData.types = json_object['types']
                i = i + 1
            for j in range(0,len(sock)):
                receive_and_send_messages(sock[j],addr[j],agentData.name)
                print("CHECKING AGENT FIREWALL")
        else:
            if agentData.enabled == "TRUE":
                if platform.system() == "Windows":
                    print("Reading os logs - OS")
                    json_object = fun(agentData.name)
                    if json_object != None:
                        #agentData.name = json_object['name']
                        agentData.filePaths = json_object['filePaths']
                        agentData.level = json_object['level']
                        agentData.batch = json_object['batch']
                        agentData.port = json_object['port']
                        agentData.ports = json_object['ports']
                        agentData.enabled = json_object['enabled']
                        agentData.role = json_object['role']
                        agentData.types = json_object['types']
                else:
                    print("System is Linux")
            for file in agentData.filePaths:
                last_lines[i], json_object = send_logs_to_firewall(file,agentData.types, last_lines[i],sock,agentData.name)
                if json_object != None:
                    #agentData.name = json_object['name']
                    agentData.filePaths = json_object['filePaths']
                    agentData.level = json_object['level']
                    agentData.batch = json_object['batch']
                    agentData.port = json_object['port']
                    agentData.ports = json_object['ports']
                    agentData.enabled = json_object['enabled']
                    agentData.role = json_object['role']
                    agentData.types = json_object['types']
                i = i + 1
        print(agentData.batch)
        time.sleep(int(agentData.batch))