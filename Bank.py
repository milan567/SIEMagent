import os.path
import time
import random
import logging



def get_logging_messages(messages):
    messages.append("INFO|User successfully logged.")
    messages.append("INFO|User successfully logged.")
    messages.append("WARNING|Unsuccessful log atempt.")
    messages.append("WARNING|Unsuccessful log atempt.")
    messages.append("WARNING|Unsuccessful log atempt.")
    messages.append("WARNING|Unsuccessful log atempt.")


    return messages


def get_logged_messages(messages):
    messages.append("INFO|Your account balance is 20000RSD.")
    messages.append("INFO|Successfully changed password.")
    messages.append("WARNING|Unsuccessful attempt of changing password.")
    messages.append("INFO|Successfully withdrawn 2000RSD from your account.")
    messages.append("INFO|Successfully paid 2000RSD on your account.")
    messages.append("WARNING|Unsuccessful try withdraw from your account.")
    messages.append("INFO|Successfully created new account.")
    messages.append("WARNING|Your bank account has expired.")
    messages.append("WARNING|Your bank account is under your minimum level.")
    messages.append("INFO|User successfully loged out.")
    messages.append("INFO|Your account balance is 20000RSD.")
    messages.append("INFO|Successfully changed password.")
    messages.append("WARNING|Unsuccessful attempt of changing password.")
    messages.append("INFO|Successfully withdrawn 2000RSD from your account.")
    messages.append("INFO|Successfully paid 2000RSD on your account.")
    messages.append("WARNING|Unsuccessful try withdraw from your account.")
    messages.append("INFO|Successfully created new account.")
    messages.append("WARNING|Your bank account has expired.")
    messages.append("WARNING|Your bank account is under your minimum level.")
    messages.append("INFO|User successfully loged out.")
    messages.append("ERROR|Trying to change account of unloged user.")
    messages.append("ERROR|System error occured.")
    messages.append("ERROR|The bank was robbed.")
    return messages








if __name__ == '__main__':
    logging_messages = []
    unlogged_users = ['milan123','djuro95','marko14','Emulate42','momirk','sinisa','ivana43']
    logging_messages = get_logging_messages(logging_messages)
    logged_users = []
    logged_messages = []
    logged_messages = get_logged_messages(logged_messages)



    logging.basicConfig(filename="Bank.log", level=logging.INFO,
                        format="%(id)s|%(asctime)s|%(ip)s|%(host)s|%(facility)s|%(levelname)s|%(tag)s|%(message)s")

    id = 0

    logFile = open("Bank.log")
    lines = logFile.readlines()
    if len(lines) != 0:
        id = int(lines[-1].split("|")[0])
    logFile.close()


    while True:
        id = id + 1
        if len(unlogged_users) != 0:
            i = random.randint(0, len(unlogged_users)-1)
            j = random.randint(0, len(logging_messages)-1)
            data = logging_messages[j].split("|")
            while data[0] != "INFO":
                logging.warning(data[1], extra={"id": id, "ip": "192.108.64.128", "host": "host1", "facility": "daemon",
                                         "tag": unlogged_users[i]})
                j = random.randint(0, len(logging_messages) - 1)
                data = logging_messages[j].split("|")
            data = logging_messages[j].split("|")
            logging.info(data[1], extra={"id": id, "ip": "192.108.64.128", "host": "host1", "facility": "daemon",
                                    "tag": unlogged_users[i]})
            logged_users.append(unlogged_users[i])
            unlogged_users.remove(unlogged_users[i])
        if len(logged_users) != 0:
            i = random.randint(0, len(logged_users)-1)
            j = random.randint(0, len(logged_messages)-1)
            data = logged_messages[j].split("|")
            if data[0] == "INFO":
                logging.info(data[1], extra={"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":logged_users[i]})
                if data[1] == "User successfully loged out.":
                    unlogged_users.append(logged_users[i])
                    logged_users.remove(logged_users[i])
            elif data[0] == "WARNING":
                logging.warning(data[1], extra={"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":logged_users[i]})
            else:
                logging.error(data[1], extra= {"id":id, "ip":"192.108.64.128","host":"host1","facility":"daemon","tag":logged_users[i]})
        time.sleep(5)




