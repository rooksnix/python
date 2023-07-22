# a simple Python 3 program which is able to correlate IPv4 and IPv6 addresses, to actual street addresses. The program should be able to append data as it changes over time. Should libraries be called, ensure they are always kept compatible.
# 
# To correlate IPv4 and IPv6 addresses to street addresses, you can use the GeoIP2 library in Python. This library allows you to perform IP geolocation and retrieve location information based on IP addresses.
# 
# First, you need to install the geoip2 library. Open your terminal and run the following command:
# pip install geoip2

import geoip2.database

# Path to the GeoIP2 database file
DATABASE_FILE = "GeoIP2-City.mmdb"

def get_street_address(ip):
    reader = geoip2.database.Reader(DATABASE_FILE)
    try:
        response = reader.city(ip)
        street_address = response.city.name + ", " + response.subdivisions.most_specific.name + ", " + response.country.name
        return street_address
    except geoip2.errors.AddressNotFoundError:
        return "Unknown"

def append_data(ip, street_address):
    with open("ip_addresses.txt", "a") as file:
        file.write(f"{ip}: {street_address}\n")

# Example usage
# ip = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
# street_address = get_street_address(ip)
# append_data(ip, street_address)
# print(f"Street address for {ip}: {street_address}")

# In this program, we define the get_street_address function, which takes an IP address as input 
# and returns the corresponding street address. It uses the geoip2.database.Reader class to read
# the GeoIP2 database file and performs a lookup for the given IP address. 
# If the address is found, it constructs the street address using the retrieved location information. 
# If the address is not found, it returns "Unknown".
# The append_data function is used to append the IP address and its corresponding street address to a text file. The IP address and street address are written in the format "IP: Street Address".
# You can modify the program according to your needs, such as reading IP addresses from a file or integrating it into a larger application. Just make sure to provide the path to the GeoIP2 database file (e.g., GeoIP2-City.mmdb) and handle any exceptions that may occur during the lookup.
# Remember to keep the geoip2 library up to date to ensure compatibility. You can update it by running pip install --upgrade geoip2 when a new version becomes available.

2)

#  
#  name: unknown
#  @param
#  @return
#  
#better linux perf and networking scrpt with graphing etc to allow the user
#to slice and dice by time or issue type and diagnostics built in .
#Have the script analyse the logging based on:
	
#- rhel 7 tuning guide $headings and correlate each section against current and possible 
#parameters
#The script should be instatiated by the user running the bash shell and executing the command with inpout
#parameters of sosreport, sar, networking and other logging
#If i can include recommendations based on input files thats cool
#maybe compare proc and sysfs for correlation
#use sysctl.conf and associated kernel doco to drive out the best practive recommendations

3)
#A script or python to analyse packet captures and provide highly intelligent feedback on network issues.

4) 
#Script which will retrieve data from all news channels and format a mobile app that....

5) 
#An app built around teslas paranormal (and other) available patents?

