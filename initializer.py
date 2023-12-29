import netmiko
import telnetlib
from getpass import getpass
from paramiko.ssh_exception import SSHException
import time

class initializer():
    def __init__(self):
        self.username = input("Enter remote access username: ")
        print("Please enter your remote access password.\n")
        self.password = getpass()

    def connectSSH(self, ipformat):

        try:
            device = netmiko.ConnectHandler(**ipformat)  # accepts arguments that go by 'Key': 'Value', which essentialls accepts credentials and other important information
        except netmiko.NetMikoTimeoutException:
            print("Device " + ipformat["ip"] + " SSH attempt timed out.")
            return
        except netmiko.NetMikoAuthenticationException:
            print("Device " + ipformat["ip"] + " Failed SSH login authentication during atempt.")
            return
        except SSHException:
            print("Device " + ipformat["ip"] + " Couldn't be accessed with SSH. Did you configure SSH on this device?")
            return
        except Exception as e:
            print("A unknown error has been encounterd with device " + ipformat["ip"] + ". Error: " + str(e))
            return
        return device

    def connectTelnet(self,ip):
        # some important variables for telnet to work in my case
        waitPeriod = 2

        tn = telnetlib.Telnet(ip)  # establishes the telnet session with host

        # AUTHENTICATION PROCESS
        tn.read_until(b"Username: ")  # reads telnet session until it sees the line "Username: " on cli. VARIES ON THE AUTHENTICATION OUTPUT
        time.sleep(waitPeriod)
        tn.write(self.username.encode("ascii") + b"\n")  # converts username var to ascii and adds an enter to it

        # checks if there is a password in the password var
        if self.password:
            tn.read_until(b"Password: ")
            time.sleep(waitPeriod)
            tn.write(self.password.encode("ascii") + b"\n")

        return tn
