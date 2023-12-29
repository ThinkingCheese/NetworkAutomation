import sys
import time
sys.path.append("../")
from initializer import initializer

# MAKE SURE CONFIG ON DEVICE IS CORRECT AND MANUAL TELNET SESSION IS ALL GOOD
# Information gathering

waitPeriod = .2


def performtelnet(info):
    print("Configuring Network-Device " + info[0])
    # CONFIGURATION PROCESS (once the telnet session is successful)
    tn = telnet.connectTelnet(info[0])

    #  !!!!  *enter enable password here  !!!!

    # CONFIGURATION THROUGH 'RouterConfig.txt' FILE
    if info[1] == "router":
        config = open("RouterConfig.txt", "r")
        for configline in config:  # goes through each line
            configline = configline.encode("ascii") + b"\r\n"
            time.sleep(waitPeriod) # because it's too damn fast!!
            tn.write(configline)  # encodes line into ascii for terminal and inputs command, along with enter
        config.close()
        print("Successful telnet to Router " + info[0])
        return
    # otherwise, if it's switch
    config = open("SwitchConfig.txt", "r")
    for configline in config:  # goes through each line
        configline = configline.encode("ascii") + b"\r\n"
        time.sleep(waitPeriod)  # because it's too damn fast!!
        tn.write(configline)  # encodes line into ascii for terminal and inputs command, along with enter
    config.close()
    print("Successful telnet to Switch " + info[0])


# Initialization process
try:
    print("Telnet Install Config Automation Script")
    print("Please ensure telnet has been properly configured before using this script.")

    telnet = initializer()  # requests user and password + telnet + ssh functionality

    # opening text file with ip address of network devices to configure
    devices = open("devices.txt")

    # Devices text file should be formatted in each line as (for example): "192.168.1.1,[router/switch]"

    for devicesIP in devices:
        devicesIP = devicesIP.strip().split(",")
        performtelnet(devicesIP)

    devices.close()
    print("Configuration of all devices successful!")
except IndexError:
    print("Index out of range error. Did you enter the proper information in the devices.txt file? i.e \"192.168.1.1,[router/switch]\"")
except Exception as e:
    print("Unknown error occured. Error: " + str(e))