import os.path
import time
import random
import logging



def errors(messages):
    messages.append("ERROR|Message was not delivered.")
    messages.append("ERROR|Can not load messages.")
    messages.append("ERROR|Message was not sent.")
    messages.append("ERROR|Contact does not exist.")
    messages.append("ERROR|Message was deleted.")
    return messages


def warnings(messages):
    messages.append("WARNING|Message is too large.")
    messages.append("WARNING|Message may contain a virus.")
    messages.append("WARNING|It is not recomended to open this message.")
    messages.append("WARNING|This message may harm your computer.")
    messages.append("WARNING|This person is not in your contact list.")
    return messages


def info(messages):
    messages.append("INFO|Message sent.")
    messages.append("INFO|Message delivered.")
    messages.append("INFO|Message received.")
    messages.append("INFO|Message seen.")
    messages.append("INFO|New contact was added.")
    return messages


def debug(messages):
    messages.append("CRITICAL|Unexpected ip address of loged user.")
    messages.append("CRITICAL|Received message contains code.")
    return messages






if __name__ == '__main__':
    messages = []
    errors(messages)
    warnings(messages)
    info(messages)
    debug(messages)

    logging.basicConfig(filename="Messenger.log", level=logging.INFO,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

    id = 0

    logFile = open("Messenger.log")
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




