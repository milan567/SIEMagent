import os.path
import time
import random
import logging



def errors(messages):
    messages.append("ERROR|A rule has been deleted in the Windows Firewall exception list.")
    messages.append("ERROR|Windows could not start the Windows Firewall on Local Computer. For more information, review the System Event Log.")
    messages.append("ERROR|Access denied")
    messages.append("ERROR|Connection is blocked")
    return messages


def warnings(messages):
    messages.append("WARNING|This file may harm your computer.")
    messages.append("WARNING|Windows firewall has blocked some features of this program.")
    messages.append("WARNING|Your computer has virus.")
    messages.append("WARNING|Firewall has blocked a program from accessing the internet.")
    messages.append("WARNING|Firewall breach detected")
    return messages


def info(messages):
    messages.append("INFO|Windows defender firewall is on.")
    messages.append("INFO|Inbound conections that do not match a rule are blocked.")
    messages.append("INFO|Outbound conections that do not match a rule are allowed")
    messages.append("INFO|Firewall notifications are enabled.")
    messages.append("INFO|Windows is connected to wi-fi.")
    return messages


def debug(messages):
    messages.append("CRITICAL|Wiindows firewall is not using recommended setings to protect your computer.")
    messages.append("CRITICAL|Your sistem detected some unusual activity.")
    return messages






if __name__ == '__main__':
    messages = []
    errors(messages)
    warnings(messages)
    info(messages)
    debug(messages)

    logging.basicConfig(filename="Firewall.log", level=logging.INFO,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

    id = 0

    logFile = open("Firewall.log")
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




