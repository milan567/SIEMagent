import os.path
import time
import random
import logging



def errors(messages):
    messages.append("ERROR|Could not connect camera.")
    messages.append("ERROR|Could not connect michropone.")
    messages.append("ERROR|Internet connection lost.")
    return messages


def warnings(messages):
    messages.append("WARNING|This is not the lattest version.")
    messages.append("WARNING|Internet connection is low.")
    messages.append("WARNING|Video connection is low.")
    messages.append("WARNING|This person is not in your contact list.")
    messages.append("WARNING|This contact is deleted.")
    return messages


def info(messages):
    messages.append("INFO|Camera is enabled.")
    messages.append("INFO|Camera is disabled.")
    messages.append("INFO|Michropone is enabled.")
    messages.append("INFO|Michropone is disabled.")
    messages.append("INFO|New contact was added.")
    return messages


def debug(messages):
    messages.append("CRITICAL|Unexpected ip address of logged user")
    messages.append("CRITICAL|Someone is trying to acces to your account.")
    return messages






if __name__ == '__main__':
    messages = []
    errors(messages)
    warnings(messages)
    info(messages)
    debug(messages)

    logging.basicConfig(filename="Skype.log", level=logging.INFO,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

    id = 0

    logFile = open("Skype.log")
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




