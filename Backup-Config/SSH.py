import os
from time import strftime
import sys
sys.path.append("../")
from initializer import initializer

# MAKE SURE CONFIG ON DEVICE IS CORRECT AND MANUAL TELNET SESSION IS ALL GOOD
# Information gathering

waitPeriod = .5


def performSSH(hostDev):
    print("Configuring Network-Device " + hostDev["ip"])

    sshsession = ssh.connectSSH(hostDev)
    #  !!!!  *enter enable password here  !!!!E
    configoutput = None
    # Find out the type of device! (WIP??)
    if hostDev["device_type"] == "cisco_ios":
        configoutput = sshsession.send_command("show run")
    elif hostDev["device_type"] == "juniper":
        configoutput = sshsession.send_command("show run") # not actual command
    configbackupdir = os.path.expanduser("~") + "/Documents/Configuration-Backup/"
    if not os.path.exists(configbackupdir):
        print("Backup folder not found, creating..")
        os.mkdir(configbackupdir)

    backup = open(configbackupdir + hostDev["ip"] + " Config Backup.txt", "a")
    backup.write("\nBackup of " + hostDev["ip"] + ", DATE: " + strftime("%Y-%m-%d %H:%M:%S") + "\n")
    backup.write(str(configoutput) + "\n")
    backup.close()

    print("Successful SSH to " + hostDev["ip"])


# Initialization process
try:
    print("SSH Install Config Automation Script")
    print("Please ensure SSH has been properly configured before using this script.")

    # getting credentials prior to config
    ssh = initializer()

    infoFormat = {
        "device_type": "cisco_ios",
        "ip": "nil",
        "username": ssh.username,
        "password": ssh.password
    }

    with open("devices.txt", "r") as file:
        devicesiptable = file.read().splitlines()

    for info in devicesiptable:
        info = info.strip().split(",")
        infoFormat["ip"] = info[0]
        infoFormat["device_type"] = info[1]
        performSSH(infoFormat)

    # opening text file with ip address of network devices to configure

    print("Configuration of all devices successful!")
except IndexError:
    print("Index out of range error. Did you enter the proper information in the devices.txt file? i.e \"192.168.1.1,[router/switch]\"")
except Exception as e:
    print("Unknown error occured. Error: " + str(e))
