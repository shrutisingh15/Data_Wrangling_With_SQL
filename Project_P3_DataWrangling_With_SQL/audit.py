
# coding: utf-8

# ### OpenStreetMap Project P3 : Data Wrangling of Syracuse City Area Using SQL : Auditing

# In[4]:

# Importing all the required libraries
import csv
import codecs
import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint


# In[5]:

# All the files needed
OSM_PATH="syracuse_new-york.osm"


# ### Auditing Street names

# In[7]:

# Code to check for common errors in street types


# Function to get the street names from the xml tag elements.

def is_street_name(tag):            
    return (tag.attrib['k'] == 'addr:street')


# List of expected street types

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Close", "Circle", "Lorong", "Crescent", "Hill", "Highway",
            "Heights", "Link", "Loop", "Park", "Terrace", "View", "Walk", "Way", "Turnpike", "Parkway", 
           "Plaza", "Path", "Center", "Route", "Trail", "Rowe", "Ridge", "31"]

# Dictionary of mapping between the expected street types and common errors that can be encountered in the osm document

mapping = {
    "St":"Street",
    "St.":"Street",
    "St ":"Street",
    "street":"Street",
    "Ave":"Avenue",
    "Av":"Avenue",
    "Rd":"Road",
    "Rd.":"Road",
    "road":"Road",
    "Pl":"Place",
    "place":"Place",
    "terrace":"Terrace",
    "Ln": "Lane",
    "Dr": "Drive",
    "Pkwy":"Parkway",
    "Cir":"Circle",
    "Plz":"Plaza",
    "Rte" : "Route",
    "Courts":"Court"

    
}


PROBLEMCHARS = re.compile(r'[=\+-/<>;"\?%#$@\,\r\n]')

# Function to audit the street names by validating their street types.

def audit_street_name():
    with open(OSM_PATH,'r') as f:
        for _,elem in ET.iterparse(f):
            if elem.tag == 'node' or elem.tag == 'way':
                 for tag in elem.iter('tag'):
                    if is_street_name(tag):
                        street_name = tag.attrib['v']
                        if PROBLEMCHARS.search(street_name):
                            print 'Street name with problem chars: {}'.format(street_name)
                        st_name=street_name.split(' ')    # Splitting the street name 
                        if st_name[-1] not in expected:   # Checking the street types
                            if st_name[-2] not in expected:  # Another condition to check street types, as sometimes
                                                             # street types are present in the middle and not in the last position
                                                             # of the full street name.
                                print 'Mis typed Street name: {}' .format(street_name)
                                if st_name[-1] in mapping:
                                    correct_st_name=mapping[st_name[-1]]
                                    st_name[-1]=correct_st_name
                                    street_name=' '.join(st_name)   # Joining the correct street type and to the main name of the street
                                    print 'Correct Street name: {}'.format(street_name)
    return None


if __name__ == '__main__':
    audit_street_name() 


# ### Auditing Postal Codes

# In[8]:

# Code to check for issues in Postal Codes


# List of Syracuse Postal Codes

Syracuse_PostalCodes=['13201','13202','13203','13204','13205','13206','13207','13208','13209','13210','13211','13212',
                     '13214','13215','13217','13218','13219','13220','13221','13224','13225','13235','13244','13250','13251',
                      '13252','13261','13290']

# Function to audit Postal Codes

def audit_postalcode():
    problemchars = re.compile(r'[=\+-/&<>;\'"\?%#$@\,\. \t\r\n]')
    with open(OSM_PATH,'r') as f:
         for _,elem in ET.iterparse(f):
                if elem.tag == 'node' or elem.tag == 'way':
                    for tag in elem.iter('tag'):
                        if tag.attrib['k'] == 'addr:postcode':
                            postalcode=tag.attrib['v']
                            m=problemchars.search(postalcode)
                            if m:
                                print 'Postal code with last four digits : {}'.format(postalcode) # Condition to check the last four digits.
                                post=postalcode.split('-')
                                postalcode=post[-2]
                                print 'Correct Postal code: {}'.format(postalcode) 
                            if not postalcode.isdigit():                # Condition to check the presence of only digits.
                                print 'Bad codes: {}'.format(postalcode)
                            if len(postalcode) > 5:              # Condition to check the length of postal codes.
                                print 'Postal code with more than 5 digits: {}'.format(postalcode)
                                postalcode = postalcode[0:5] 
                                print 'Correct Postal code: {}'.format(postalcode)
                            if postalcode not in Syracuse_PostalCodes:  # Condition to check the Postal codes of Syracuse City.
                                print 'Postal Code for another city: {}'.format(postalcode)
    return None


if __name__ == '__main__':
    audit_postalcode()


# In[ ]:



