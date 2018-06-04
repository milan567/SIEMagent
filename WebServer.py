import os.path
import time
import random
import logging



def errors(messages):
    messages.append("ERROR|Starting general service timed out.")
    messages.append("ERROR|Starting database service timed out.")
    messages.append("ERROR|Service lost connection.")
    messages.append("ERROR|Security certificate date is not valid.")
    messages.append("ERROR|Server not found.")
    return messages


def warnings(messages):
    messages.append("WARNING|Saved SSL Certificate")
    messages.append("WARNING|Missing resource message key")
    messages.append("WARNING|Connection may be insecure.")
    messages.append("WARNING|Secure connection failed.")
    return messages


def info(messages):
    messages.append("INFO|General service started.")
    messages.append("INFO|License validility: TRUE")
    messages.append("INFO|General service starting.")
    messages.append("INFO|Event service wrapper started.")
    messages.append("INFO|Database service starting")
    return messages


def debug(messages):
    messages.append("CRITICAL|Database conection lost.")
    messages.append("CRITICAL|Not possible to start server.")
    return messages






if __name__ == '__main__':
    messages = []
    errors(messages)
    warnings(messages)
    info(messages)
    debug(messages)

    logging.basicConfig(filename="WebServer.log", level=logging.INFO,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

    id = 0

    logFile = open("WebServer.log")
    lines = logFile.readlines()
    if len(lines) != 0:
        id = int(lines[-1].split("|")[0])
    logFile.close()


    while True:
        id = id + 1
        i = random.randint(0, len(messages)-1)
        data = messages[i].split("|")
        if data[0] == "INFO":
            logging.info(data[1], extra={"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":"tinyproxy[9456]"})
        elif data[0] == "CRITICAL":
            logging.critical(data[1], extra={"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":"tinyproxy[9456]"})
        elif data[0] == "WARNING":
            logging.warning(data[1], extra={"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":"tinyproxy[9456]"})
        else:
            logging.error(data[1], extra= {"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":"tinyproxy[9456]"})
        time.sleep(30)




