# Python 3.6
# Made to run on Windows at command prompt
# the main function runs it all and calls the other functions

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from getpass import getpass
import re


platform = 'cisco_wlc'
fopen = open('ap_host.txt', 'r')
hosts = fopen.read().splitlines()
username = 'admin'                   #####Edit this for your username##########
password = getpass.getpass("Please enter the password for the WLCs: " )


def main():
    for i in hosts:
        net_connect = connect_to_host(i)  # connect to host
        aps = get_aps(net_connect)
        get_count(aps)

def get_count(ap_list):
        sites=[]
        #dictionary to store the aps in
        ap_dict={}
        out_csv = 'ap_count.csv'
        #get the ap list and just get the three digit site codes from it
        for i in ap_list:
            print (i)
            #We use three digit site IDs to name the APs, edit the regex for your naming scheme 
            x = re.match('\d\d\d', i)
            if x:
                sites.append(x.group() + '\n')
        #count the number of times each site code appears, one for each ap
        for site in sites:
            if  ap_dict.has_key(site) == False:
                ap_dict[site] = 1
            elif ap_dict.has_key(site) == True:
                _ctr = int(ap_dict[site])
                _ctr += 1
                ap_dict[site] = _ctr
        #open the csv and write the site code and ap count
        with open(out_csv, 'a') as outfile_csv:
            for x in ap_dict:
                y = str(ap_dict[x])
                y = y.rstrip()
                z = str(x)
                z = z.rstrip('\n')
                out_string = z + ',' + y
                outfile_csv.write(out_string + '\n')

def getHostname(net_connect):
    #get the hostname and assign it to the host variable
    host = net_connect.find_prompt()
    #return the hostname but strip out the pound sign so it can be used for labelling
    return host.replace("#", '')

def get_aps(connect):
    #the command to send to the controller
    c_command = 'sh ap summary'
    #send the command to the controller
    raw_output = connect.send_command(c_command)
    # extract the macs
    output_lines = raw_output.split('\n')
    #list to store the output in, and return this array when completed
    out_list = []
    #the output of the command returns values with different number of fields so these are all needed to get all the output and lose whats left
    for x in output_lines:
        line_split = x.split()
        #different line lengths are retuned by the WLC so each must be accounted for to get accurate list of all the APs
        if len(line_split) == 13:
            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen = line_split
            # ap_name, slots, ap_model, mac_addr, location, country, ip_addr, clients, dse_location = line_split
            out_list.append(one)
        if len(line_split) == 14:
            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen = line_split
            # ap_name, slots, ap_model, mac_addr, location, country, ip_addr, clients, dse_location = line_split
            out_list.append(one)
        if len(line_split) == 12:
            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve = line_split
            # ap_name, slots, ap_model, mac_addr, location, country, ip_addr, clients, dse_location = line_split
            out_list.append(one)
        if len(line_split) == 15:
            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen = line_split
            # ap_name, slots, ap_model, mac_addr, location, country, ip_addr, clients, dse_location = line_split
            out_list.append(one)
    return out_list

def connect_to_host(_ip):
    #try to connect to the host, return an error if unable to connect
    try:
        return ConnectHandler(device_type=platform, username=username, ip=_ip, password=password)
    except(NetMikoTimeoutException):
        print (str(_ip) + ' is not reachable')
    except(NetMikoAuthenticationException):
        print (' Cannot connect . . . bad username or password')

if __name__ == "__main__":
    main()
