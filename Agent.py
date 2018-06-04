import io
import numpy as np
import time
import requests
from datetime import datetime
import urllib
import json
import ssl
import httplib2



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
        b = json.dumps(data).encode('utf-8')
        print(b)
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
                    print(elements[1][:19])
                    datetime_object = datetime.strptime(elements[1][:19], "%Y-%m-%d %H:%M:%S")
                    print(datetime_object)
                    l = Log(elements[5],elements[7],datetime_object,elements[2],elements[3]
                            ,elements[4],elements[6])
                    self.send_post_request(l)
                else:
                    print("Not sending.")
                index = index + 1
        return len(lines)




if __name__ == '__main__':

    separator = "="
    keys = {}
    '''
        sc = pyspark.SparkContext()
        sc.setSystemProperty("javax.net.ssl.keyStore" , "C:\\Users\\milan\\Desktop\\Salic\\Bezbjednost\\BS\\keystore.jks")
        sc.setSystemProperty("javax.net.ssl.keyStorePassword", "admin1234");
        sc.setSystemProperty("javax.net.ssl.trustStore", "C:\\Users\\milan\\Desktop\\Salic\\Bezbjednost\\BS\\myTrustStore.jts");
        sc.setSystemProperty("javax.net.ssl.trustStorePassword", "admin1234");
    '''
    # I named your file conf and stored it
    # in the same directory as the script

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
    print(last_lines)
    a = Agent()
    while True:
        i = 0
        for file in files:
            last_lines[i] = a.send(file, types, last_lines[i])
            i = i + 1
        time.sleep(5)