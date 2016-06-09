
## OpenStreetMap Project

### Map Area : Syracuse City Area, New York, USA 

### Introduction :
I choose to analyse Syracuse City and area around it because it was fitting in the minimum dataset size requirement. The OSM file size is 61 MB in uncompressed form.Syracuse is the fourth most populous metropolitan city in the state of New York, U.S.A.
It is the economic and educational hub of Central New York, a region with over a million inhabitants.

### Problems Encountered:

I kick started my analysis by exploring for the common errors in street names and postal codes by running the audit_street_name() and audit_postalcode() function codes against the dataset.The following errors were encountered by me :

#### 1.Abbreviations and typo error in street names:
Abbreviations and typos were present in the street names like 'James St.' and 'Presidential Courts'.I corrected such data items by using a standard mapping dictionary that I created in the audit_street_name() codes.
#### 2. Wrong format of the key & type fields in node_tags and way_tags:
After importing the data in SQL database,I ran couple queries to check the format specified for the key and type columns in way_tags and node_tags tables.


sqlite>SELECT * FROM node_tags WHERE key LIKE '%:%' AND type = 'regular' UNION ALL SELECT * FROM way_tags WHERE key LIKE '%:%' AND type = 'regular';

The results showed the presence of records that still had wrong format of the type and key columns like key='gnis:ST_alpha' and type ='regular' or key ='currency:USD' and type = 'regular' or key= 'gnis:ST_num' and type='regular'.There were quite many records with this type of issue. This was happened despite of running the formatting code in the shape_element() code as follows:


For node_tags:

if not PROBLEMCHARS.search(tag.attrib['k']):
    if LOWER_COLON.search(tag.attrib['k']):
            sub=tag.attrib['k'].split(':',1)
            key=sub[-1]
            typev=sub[-2]
                                
                               
For way_tags:

if not PROBLEMCHARS.search(tag.attrib['k']):
    if LOWER_COLON.search(tag.attrib['k']):
            sub=tag.attrib['k'].split(':',1)
            keyval=sub[-1]
            typeval=sub[-2]
Hence, I ran couple update queries like the following in the SQL database itself to correct the format.
sqlite> UPDATE node_tags
SET key = 'Class',type='gnis'
WHERE key = 'gnis:Class' AND type = 'regular';

####  3. Issues in Postal codes : 
* Bad Postal code(values with more than 5 digits) like "132059211" , "132179211" were found.I cleaned such values by truncating the last extra digits and also checked if the postal values exist in the City of Syracuse.

* Also, there was no consistency in  the postal code values of many records.That means there were records in which hyphen with the last four digits were also present like "13202-1107", "13210-1203".I cleaned up such values to make sure all the records have the same 5 digit format and are correct.

* Moreover, the codes for Syracuse city should begin with "132".I ran the following query to check for the same:

sqlite>SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM node_tags 
      UNION ALL 
      SELECT * FROM way_tags) tags
WHERE tags.key='postcode'
GROUP BY tags.value
ORDER BY count DESC;


The dataset has other value codes also that begin with '130' and '131' like the following results.The records for surrounding areas of Syracuse city were also present.

13224|821
13214|513
13210|475
13205|282
13206|279
13108|171
13212|136
13057|114
13031|112
13066|110
13104|101
13202|93
13215|78
13204|75
13088|64
13208|50
13203|45
13209|43
13164|40
13219|32
13078|17
13039|16

So, I ran another query to sort the cities by count.

#### Sort cities by count in descending order:
sqlite> SELECT tags.value, COUNT(*) as count 
FROM (SELECT * FROM node_tags UNION ALL 
      SELECT * FROM way_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;


And the results were as follows :

Syracuse           2834
DeWitt             808
Marcellus          209
Camillus           158
Fayetteville       116
Manlius            104
North Syracuse     104
East Syracuse      94
Liverpool          69
Solvay             35
Cicero             29
Dewitt             26
Onondaga           25
Jamesville         15
tiger              12
Salina             8
10                 5
1                  4
Mattydale          4
100                3
2                  3
4                  3
6                  3
8                  3
Baldwinsville      3
Nedrow             3
Onondaga Nation    3
12                 2
20                 2
200                2
39.5 MW            2
80                 2
Clay               2
Mattdale           2
1000               1
104                1
109                1
1250               1
13                 1
1345               1
170                1
20-30              1
220                1
23                 1
280                1
285                1
375                1
425                1
5                  1
50                 1
520                1
550                1
560                1
575                1
70                 1
75                 1
77                 1
800                1
98                 1
Auburn             1
Bridgeport         1
East Syracuse, NY  1
Fulton             1
Kirkville          1
Minoa              1
east Syracuse      1


Clearly, the results indicate the presence of surrounding areas of Syracuse City as well, as shown by the postalcodes.
### Data Overview and Additional Ideas:

#### File Sizes :
Syracuse.osm ............... 61 MB
Syracuse.db ................ 35.4 MB
nodes.csv .................. 21.9 MB
node_tags.csv .............. 1.31 MB
ways.csv ................... 1.94 MB
ways_nodes.csv ............. 7.40 MB
ways_tags.csv .............. 5.71 MB
#### Number of nodes :
sqlite> SELECT COUNT(*) FROM nodes;
278790

#### Number of ways :
sqlite> SELECT COUNT(*) FROM way;
35363

#### Number of unique users :
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM way) e;
229

#### Top 10 contributing users :
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM way) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;zeromap          158155
woodpeck_fixbot  75599
DTHG             27981
yhahn            8129
RussNelson       8073
fx99             4495
bot-mode         4410
timr             2859
TIGERcnl         2077
Johnc            2035
#### Number of users appearing only once (having 1 post)
sqlite> SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM way) e
     GROUP BY e.user
     HAVING num=1)  u;
50

### Additional Ideas

#### Contributor statistics and gamification suggestion
The overall participation of users is skewed as shown by the top 10 contributing users.Use of automated edits or semi-automated edits by bots might be the possible factors for the skewed user participation statistics.

* The top user "zeromap" contributed 50.34%.
* The top 2 users "zeromap" and "woodpeck_fixbot" contributed 74.40%.
* The top 10 users contributed 93.52%.

The above statistics makes me ponder of gamification as one of the reasons behind such contributions.Gamification is a service that gamifies the collection of data in OpenStreetMaps.It engages & motivates users to showcase their talents or desires by including rewards schemes like Badges and Points.In this way,gamification can used as a service to attract more contribution by users who contribute once or twice or not very often as they can use gamified check-ins when ever they go a new location.
In this age when nearly all the social networking apps(like facebook and whatsapp)have location check-in feature, users can keep adding new location information easily through their smart phones and that data will be more accurate because of the GPS data capturing feature of the smart phone.

Although gamification rewards like points or badges can have a positive effect on user attitude towards submitting more data, but there are still doubts in its real efficacy.Like, it can be very effective for users' goal oriented and social behaviours but vanish in utilitarian services.So, we can say gamification can't drive long term behavorial change.It works but only to a certain degree.


#### Number of unique sources of data
sqlite> SELECT COUNT(DISTINCT tags.value)
FROM (SELECT * FROM node_tags UNION ALL SELECT * FROM way_tags) tags
WHERE tags.type = 'source';78

#### Top 10 sources of data
sqlite> SELECT tags.value ,COUNT(*) as count
FROM (SELECT * FROM node_tags UNION ALL SELECT * FROM way_tags) tags
WHERE tags.type='source'
GROUP BY tags.value
ORDER BY count DESC
LIMIT 10;NYSDOT https://www.dot.ny.gov/divisions/operating/oom/transportation-systems/repository/2010%20trk%20access%20bk.pdf.... 758
TIGER 2015 ............................................................................................................. 576
survey ................................................................................................................. 182
tiger 2015 ............................................................................................................. 64
tiger .................................................................................................................. 24
National Transportation Atlas Database 2011 ............................................................................ 22
local knowledge ........................................................................................................ 19
Tiger 2015 ............................................................................................................. 17
receipt ................................................................................................................ 12
JOSM Incomplete Address plugin ......................................................................................... 8
### Additional Data Exploration

#### Top 10 appearing amenities
sqlite> SELECT value, COUNT(*) as num
FROM node_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;school            152
bench             151
fast_food         93
restaurant        75
place_of_worship  73
post_box          55
bicycle_parking   49
waste_basket      37
pharmacy          31
cafe              30
#### Biggest Religion 
sqlite> SELECT node_tags.value, COUNT(*) as num
FROM node_tags 
    JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value='place_of_worship') i
    ON node_tags.id=i.id
WHERE node_tags.key='religion'
GROUP BY node_tags.value
ORDER BY num DESC
LIMIT 1;Christian   69
#### Most Popular Cuisines
sqlite> SELECT node_tags.value, COUNT(*) as num
FROM node_tags 
    JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value='restaurant') i
    ON node_tags.id=i.id
WHERE node_tags.key='cuisine'
GROUP BY node_tags.value
ORDER BY num DESC;pizza               11
chinese             8
american            7
italian             3
steak_house         3
burger              2
japanese            2
mexican             2
sandwich            2
Waffles             1
diner               1
german              1
greek               1
hispanic            1
indian              1
jamaican            1
korean;japanese     1
mediterranean       1
seafood             1
thai                1
vietnamese          1
#### Number of coffee shops
sqlite> SELECT node_tags.value, COUNT(*) as num
FROM node_tags
JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value='cafe') i
ON node_tags.id=i.id
WHERE node_tags.key='amenity'
GROUP BY node_tags.value
ORDER BY num DESC;cafe|30
#### Top 3 coffee shops
sqlite> SELECT node_tags.value, COUNT(*) as num
FROM node_tags
JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value LIKE '%cafe%') i
ON node_tags.id=i.id
WHERE node_tags.key='name'
GROUP BY node_tags.value
ORDER BY num DESC;Dunkin Donuts    8
Cafe Kubal       3
Starbucks        3
### Conclusion

While working on Syracuse city area data, I could observed lack consistent format in the data entered by users.Through my effort of auditing, cleaning and shaping the data, I expect it to cleaned well for the purpose of my analysis.As depicted in the above analysis GPS data is present in openstreetmap because of contribution of users whether by manualy entry or automated tools.Considering the merits of gamification, with the continual user efforts, we can add much cleaner and accurate data into OpenStreetMaps.

### References :

https://gist.github.com/carlward/54ec1c91b62a5f911c42#number-of-users-appearing-only-once-having-1-post

http://wiki.openstreetmap.org/wiki/Gamification

https://mapzen.com/data/metro-extracts/#syracuse-new-york

http://gameffective.com/gamification-basics/what-foursquares-evolution-can-teach-us-about-enterprise-gamification/

https://www.researchgate.net/publication/271643615_A_SWOT_Analysis_of_the_Gamification_Practices_Challenges_Open_Issues_and_Future_Perspectives




```python

```
