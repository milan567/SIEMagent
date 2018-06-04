import os.path
import time
import random
import logging



def errors(messages):
    messages.append("ERROR|The application-specific permission settings do not grant Local Activation "
                    + "permission for the COM Server application with CLSD")
    messages.append("ERROR|The driver detected a controller error on \Device\Harddisk1\DR1.")
    messages.append("ERROR|The server Microsoft.Windows.Photos did not register with DCOM within the required timeout.")
    messages.append("ERROR|The machine-default permission settings do not grant Local Activation ")
    messages.append("ERROR|The system watchdog timer was triggered.")
    return messages


def warnings(messages):
    messages.append("WARNING|The local adapter does not support an important Low Energy controller state to support peripheral mode.")
    messages.append("WARNING|Name resolution for the name"
                    + " tile-service.weather.microsoft.com timed out after none of the configured DNS servers responded.")
    messages.append("WARNING|Name resolution for the name 6.adsco.re timed out after none of the configured DNS servers responded.")
    messages.append("WARNING|Name resolution for the name mtalk.google.com timed out after none of the configured DNS servers responded.")
    messages.append("WARNING|Name resolution for the name ads.viber.com timed out after none of the configured DNS servers responded.")
    return messages


def info(messages):
    messages.append("INFO|The system has returned from a low power state.")
    messages.append("INFO|Firmware S3 times. ResumeCount: 4, FullResume: 567, AverageResume: 567")
    messages.append("INFO|The system has resumed from sleep.")
    messages.append("INFO|Power source change.")
    messages.append("INFO|Windows cannot store Bluetooth authentication codes (link keys) on the local adapter.")
    return messages


def debug(messages):
    messages.append("CRITICAL|The system has rebooted without cleanly shutting down first.")
    return messages






if __name__ == '__main__':
    messages = []
    errors(messages)
    warnings(messages)
    info(messages)
    debug(messages)

    logging.basicConfig(filename="OperatingSystem.log", level=logging.DEBUG,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

    id = 0

    logFile = open("OperatingSystem.log")
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
        time.sleep(2)




