from scapy.all import  ARP, Ether, srp,  IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf, send, ICMP, fragment, TCP
import re
from socket import *
import pyfiglet
from time import sleep
import re

# NETWORK HOST SCANNER
ascii_banner = pyfiglet.figlet_format("WILD NETWORK") 
print(ascii_banner)

pattern_ip = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]*$")
target_network = input("\nwrite the network adres to find host's in it (ex 192.168.1.0/24): ")

if pattern_ip.search(target_network):
    # IP Address for the destination
    # create ARP packet
    arp = ARP(pdst=target_network)
    # create the Ether broadcast packet
    # ff:ff:ff:ff:ff:ff MAC address indicates broadcasting
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    # stack them
    packet = ether/arp

    result = srp(packet, timeout=3)[0]
    # a list of clients, we will fill this in the upcoming loop
    clients = []

    for sent, received in result:
        # for each response, append ip and mac address to `clients` list
        clients.append({'ip': received.psrc, 'mac': received.hwsrc})

    # print clients
    print("Available devices in the network:")
    print("IP" + " "*18+"MAC")
    for client in clients:
        print("{:16}    {}".format(client['ip'], client['mac']))