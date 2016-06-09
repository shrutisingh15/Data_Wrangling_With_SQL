
# coding: utf-8

# ### OpenStreetMap Project P3 : Data Wrangling of Syracuse City Area Using SQL : Preparing the database

# In[2]:

# Importing all the required libraries
import csv
import codecs
import re
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint


# In[3]:

# All the files needed
OSM_PATH="syracuse_new-york.osm"
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"


# In[4]:

# The headers for the csv files
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

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

# List of expected street types
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Close", "Circle", "Lorong", "Crescent", "Hill", "Highway",
            "Heights", "Link", "Loop", "Park", "Terrace", "View", "Walk", "Way", "Turnpike", "Parkway", 
           "Plaza", "Path", "Center", "Route", "Trail", "Rowe", "Ridge", "31"]


# ### Updating Bad Street Names

# In[5]:

# Function to update bad street types

def update_street_name(street_name):
               
    st_name=street_name.split(' ')
    if st_name[-1] in mapping:
                correct_st_name=mapping[st_name[-1]]
                st_name[-1]=correct_st_name
    name=' '.join(st_name)
            
    return name
                                 


# ### Updating Bad Postal Codes

# In[6]:

# Function to update bad Postal codes

def update_postalcode(postalcode):
    problemchars = re.compile(r'[=\+-/&<>;\'"\?%#$@\,\. \t\r\n]')
    m=problemchars.search(postalcode)
    if m:
        post=postalcode.split('-')
        postalcode=post[-2]
    if not postalcode.isdigit():
        pass
    if len(postalcode) > 5:
        postalcode = postalcode[0:5]    
    return postalcode


# ### Shaping and updating the Elements of the OSM file

# In[7]:

# Code to shape and update the elements of OSM file

def shape_element(element):
    LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
    PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags=[]
    
    # Code to shape and update node tags & node tag items
    if element.tag == 'node':
                nodeid=element.attrib['id']      # Fetching the nodeid     
                for att in element.attrib:       # Fetching the attributes of node tag
                    node_attribs[att]=element.attrib[att]
                if element.findall('tag'):       # finding the secondary tags in the main node tag
                    for tag in element.iter('tag'):  # Iterating through the secondary tags
                        if not PROBLEMCHARS.search(tag.attrib['k']):   # Checking for the problem characters in k attribute
                            if LOWER_COLON.search(tag.attrib['k']):    # Checking for : character in k attribute
                                sub=tag.attrib['k'].split(':',1)       # Splitting the k attribute
                                key=sub[-1]
                                typev=sub[-2]
                                if tag.attrib['k'] == 'addr:street':  # Fetching the street name based on the condition
                                    street_name = tag.attrib['v'] 
                                    st_name=street_name.split(' ')
                                    if st_name[-1] not in expected:
                                        if st_name[-2] not in expected:
                                            name=update_street_name(street_name)   # updating the bad street types
                                            tag.attrib['v']=name 
                                if tag.attrib['k'] == 'addr:postcode':   # Fecthing the postal code value based on the condition
                                    postalcode=tag.attrib['v']
                                    pcode=update_postalcode(postalcode)  # updating the bad postal code values
                                    tag.attrib['v']=pcode
                                temp=dict(id=nodeid,key=key,value=tag.attrib['v'],type=typev)  
                                tags.append(temp)
                                temp=dict()
                            else:
                                temp = dict(id=nodeid,key=tag.attrib['k'],value=tag.attrib['v'],type='regular')
                                tags.append(temp)
                                temp=dict()
                else:
                    tags=[]
                return {'node': node_attribs, 'node_tags': tags}  
    # Code to shape and update way tags & way tag items
    elif element.tag == 'way':
                wayid=element.attrib['id']   # Fetching the wayid
                for att in element.attrib:   # Fetching the attributes of way tag
                    way_attribs[att]=element.attrib[att]
                if element.findall('tag'):   # Finding the secondary tags in the main way tag
                    for tag in element.iter('tag'):   #Iterating through the secondary tags
                        if not PROBLEMCHARS.search(tag.attrib['k']):   # Checking for the problem characters in k attribute
                            if LOWER_COLON.search(tag.attrib['k']):    # Checking for : character in k attribute
                                sub=tag.attrib['k'].split(':',1)      # Splitting the k attribute
                                keyval=sub[-1]
                                typeval=sub[-2]
                                if tag.attrib['k'] == 'addr:street':   # Fetching the street name based on the condition
                                    street_name = tag.attrib['v'] 
                                    st_name=street_name.split(' ')
                                    if st_name[-1] not in expected:
                                        if st_name[-2] not in expected:
                                            name=update_street_name(street_name)   # updating the bad street types
                                            tag.attrib['v']=name
                                if tag.attrib['k'] == 'addr:postcode':   # Fetching the postal code value based on the condition
                                    postalcode=tag.attrib['v']
                                    pcode=update_postalcode(postalcode)  # updating the bad postal code values
                                    tag.attrib['v']=pcode
                                temp=dict(id=wayid,key=keyval,value=tag.attrib['v'],type=typeval)
                                tags.append(temp)
                                temp=dict()
                            else:
                                temp = dict(id=wayid,key=tag.attrib['k'],value=tag.attrib['v'],type='regular')
                                tags.append(temp)
                                temp=dict() 
                else:
                    tags=[]
                if element.findall('nd'):
                    pos=0
                    for tag in element.iter('nd'):
                            temp=dict(id=wayid,node_id=tag.attrib['ref'],position=pos)
                            way_nodes.append(temp)
                            pos+=1
                return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}




# In[8]:

# Function to fetch the data from osm file iteratively

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


# In[9]:

# Function code to extend the UnicodeDictWriter class for csv file writting

class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# In[10]:

# Final code to fetch,clean and write the data in respective csv files.

def process_map(file_in):
    """Iteratively process each XML element and write to csv(s)"""
   
    with codecs.open(NODES_PATH, 'wb') as nodes_file,         codecs.open(NODE_TAGS_PATH, 'wb') as nodes_tags_file,         codecs.open(WAYS_PATH, 'wb') as ways_file,         codecs.open(WAY_NODES_PATH, 'wb') as way_nodes_file,         codecs.open(WAY_TAGS_PATH, 'wb') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
               
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])
                    
if __name__ == '__main__':
    process_map(OSM_PATH)


# In[ ]:



