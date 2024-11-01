import os
import re
import argparse
from termcolor import colored
import subprocess

#required arguments
parser = argparse.ArgumentParser()
parser.add_argument('-d', default='none', dest='domain', help='provide the domain name (eg "example.local")', type=str)
args = parser.parse_args()

#define functions
def cmdline(command):
        terminal_output = subprocess.getoutput(command)
        return(terminal_output)

#check required args completed
if args.domain == 'none':
        print(colored('\n[!] Domain not provided with \'-d\'.\n\nQuitting.','red'))
        quit()

print('[!] Scanning for domain controllers:\n')
#set the OS command
scan_cmd = 'nslookup -type=SRV _ldap._tcp.dc._msdcs.' + args.domain
#run the scan
initial_scan = cmdline(scan_cmd)
#split off and print the DNS server
server = initial_scan.split("_ldap")[0]
print(server)
#split the DCs and append to a list
dc_list = []
dc_names = []
DCs = initial_scan.split("_ldap")
for line in DCs:
    dc_list.append(line)
for line in dc_list:
    if "tcp" in line:
        domaincont = (line.split(" ")[-1])[:-1]
        print(domaincont[:-1])
        dc_names.append(domaincont)
#getting IP addresses of domain controllers
print("\n[!] Mapping domain controllers to IPs:\n")
#ping it
for line in dc_names:
    ping_cmd = 'ping ' + line + ' -c 1'
    ping_results = cmdline(ping_cmd)
    if 'bytes from' in ping_results:
        IP = ping_results.split('bytes from')[1]
        IP = IP.split(' ')[1]
        print(line[:-1] + ' : ' + IP)
    else:
        print(line[:-1] + ' : no response from ICMP packet.')
print('\nAll done! Happy hacking.')
