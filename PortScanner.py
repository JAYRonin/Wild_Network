from scapy.all import  ARP, Ether, srp,  IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf, send, ICMP, fragment, TCP
from socket import *
import threading
import re, os
from datetime import datetime
from random import randint

# HOST PORT SCANNER
def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket(AF_INET, SOCK_STREAM)
    TCPsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''

def scan_ports(host_ip, delay):

    threads = []    # To run TCP_connect concurrently
    output = {}     # For printing purposes
    timeString = datetime.now().strftime('%H:%M:%S')
    dateString = datetime.now().strftime('%d/%m/%Y')
    ports = []

    # Spawning threads to scan ports
    for i in range(1000):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output))
        threads.append(t)

    # Starting threads
    for i in range(1000):
        threads[i].start()

    # Locking the main thread until all threads complete
    for i in range(1000):
        threads[i].join()

    # Printing listening ports from small to large
    for i in range(1000):
        if output[i] == 'Listening':
            print(str(i) + ': ' + output[i])
            ports.append(str(i) + ': ' + output[i])

    # Wtrie logs to csv file
    with open(os.getcwd() + "/Logs/portScanerLogs.csv", 'a') as f:
        f.writelines(f'\n{host_ip};{dateString};{timeString};{ports}')