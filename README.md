### Cisco-WLC-AP-Count-Script

This project will connect to  Cisco Wireless Controller(s), get a count of the APs, and then write it to a csv file.

This script was created to run from a Windows command prompt and has not been tested using any other methods and may need to be edited to suit other circumstances.

It uses Netmiko to interact with the controller and return the data requested.

The IPs of the wireless controllers go into the ap_host.txt file and the script will loop through that file and query the controllers to retreieve a list of the APs currently associated with it.  I have it set up to use a regex that sorts the APs by a three digit code that we use to identify APs.  This naming convention looks like "365-FL1-AP01".  Thus the three digit regex can accurately sort the APs by site ID.  Modify this as needed.

The user name to log into the controllers is currently set as admin, change if needed.

All output is written to the screen as well as written to a csv file.
