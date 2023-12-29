import sys
import time
import os
sys.path.append("../")
from initializer import initializer

# MAKE SURE CONFIG ON DEVICE IS CORRECT AND MANUAL TELNET SESSION IS ALL GOOD
# Information gathering

waitPeriod = 1.5


def performtelnet(hostIP):
    print("Configuring Network-Device " + hostIP)

    tn = telnet.connectTelnet(hostIP)

    #  !!!!  *enter enable password here  !!!!

    # gets running conifguration
    tn.time.sleep(waitPeriod)
    tn.write(b"terminal length 0\n")
    time.sleep(waitPeriod)
    tn.write(b"show run\n")
    time.sleep(waitPeriod)
    tn.write(b"exit\n")

    config = tn.read_all().decode("ascii")
    configbackupdir = os.path.expanduser("~") + "/Documents/Configuration-Backup/"
    if not os.path.exists(configbackupdir):
        print("Backup folder not found, creating..")
        os.mkdir(configbackupdir)

    backup = open(configbackupdir + hostIP + " Config Backup.txt", "a")
    backup.write("\nBackup of " + hostIP + ", DATE: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    backup.write(config + "\n")
    backup.close()

    print("Successful telnet to " + hostIP)


try:
    # Initialization process
    print("Telnet Backup Device Config Automation Script")
    print("Please ensure telnet has been properly configured before using this script.")

    # getting credentials prior to config
    telnet = initializer()

    # opening text file with ip address of network devices to configure
    devices = open("devices.txt")

    for devicesIP in devices:
        devicesIP = devicesIP.strip().split(",")
        performtelnet(devicesIP[0])  # because there will be two args in each line in devices.txt!!

    devices.close()
    print("Backup of configuration of all devices successful! \nCheck the documents directory of your current user your logged into for the directory 'Configuration-Backup'.")


except Exception as error:
    print("There was an error while processing this script.. whoops! \n\nHere's the error: " + str(error))
    exit()
