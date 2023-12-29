import sys
sys.path.append("../")
from initializer import initializer

# MAKE SURE CONFIG ON DEVICE IS CORRECT AND MANUAL TELNET SESSION IS ALL GOOD
# Information gathering

waitPeriod = .5


def performSSH(hostDevice,network_type):
    print("Configuring Network-Device " + hostDevice["ip"])

    sshsession = ssh.connectSSH(hostDevice)
    #  !!!!  *enter enable password here  !!!!

    # CONFIGURATION THROUGH 'RouterConfig.txt' FILE
    if network_type == "router":
        with open("RouterConfig.txt", "r") as configFile:
            line = configFile.read().splitlines()
            output = sshsession.send_config_set(line)
            print(output)

        print("Successful SSH to Router " + hostDevice["ip"])
        return
    # otherwise, if it's a switch
    with open("SwitchConfig.txt", "r") as configFile:
        line = configFile.read().splitlines()
        output = sshsession.send_config_set(line)
        print(output)

    print("Successful SSH to Switch " + hostDevice["ip"])

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
        infoFormat["device_type"] = info[2]
        performSSH(infoFormat,info[1])

    # opening text file with ip address of network devices to configure

    print("Configuration of all devices successful!")
except IndexError:
    print("Index out of range error. Did you enter the proper information in the devices.txt file? i.e \"192.168.1.1,[router/switch]\"")
except Exception as e:
    print("Unknown error occured. Error: " + str(e))