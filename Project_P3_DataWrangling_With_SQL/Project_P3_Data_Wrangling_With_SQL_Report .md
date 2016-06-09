
## OpenStreetMap Project

### Map Area : Syracuse City Area, New York, USA 

### Introduction :
I choose to analyse Syracuse City and area around it because it was fitting in the minimum dataset size requirement. The OSM file size is 61 MB in uncompressed form.Syracuse is the fourth most populous metropolitan city in the state of New York, U.S.A.
It is the economic and educational hub of Central New York, a region with over a million inhabitants.

### Problems Encountered:

I kick started my analysis by exploring for the common errors in street names and postal codes by running the audit_street_name() and audit_postalcode() function codes in audit.py file against the dataset.The following errors were encountered by me :

#### 1.Abbreviations and typo error in street names:

Abbreviations and typos were present in the street names like 'James St.' and 'Presidential Courts'.I corrected such data items by using a standard mapping dictionary that I created in the audit_street_name() codes.

#### 2. Wrong format of the key & type fields in node_tags and way_tags:

After importing the data in SQL database,I ran couple queries to check the format specified for the key and type columns in way_tags and node_tags tables.

<code>
sqlite>SELECT \* FROM node_tags
WHERE key LIKE '%:%' AND type = 'regular'
UNION ALL SELECT * FROM way_tags
WHERE key LIKE '%:%' AND type = 'regular';
</code>


The results showed the presence of records that still had wrong format of the type and key columns like key='gnis:ST_alpha' and type ='regular' or key ='currency:USD' and type = 'regular' or key= 'gnis:ST_num' and type='regular'.There were quite many records with this type of issue. This was happened despite of running the formatting code in the shape_element() code as follows:


#### For node_tags:

<code>
if not PROBLEMCHARS.search(tag.attrib['k']):

     if LOWER_COLON.search(tag.attrib['k']):
     
           sub=tag.attrib['k'].split(':',1)
           
           key=sub[-1]
           
           typev=sub[-2]
 </code>                               
                               
#### For way_tags:

<code>
if not PROBLEMCHARS.search(tag.attrib['k']):

     if LOWER_COLON.search(tag.attrib['k']):
     
           sub=tag.attrib['k'].split(':',1)
           
           keyval=sub[-1]
           
           typeval=sub[-2]
</code>

Hence, I ran couple update queries like the following in the SQL database itself to correct the format.

<code>
sqlite> UPDATE node_tags
SET key = 'Class',type='gnis'
WHERE key = 'gnis:Class' AND type = 'regular';
</code>

####  3. Issues in Postal codes : 

* Bad Postal code(values with more than 5 digits) like "132059211" , "132179211" were found.I cleaned such values by truncating the last extra digits and also checked if the postal values exist in the City of Syracuse.

* Also, there was no consistency in  the postal code values of many records.That means there were records in which hyphen with the last four digits were also present like "13202-1107", "13210-1203".I cleaned up such values to make sure all the records have the same 5 digit format and are correct.

* Moreover, the codes for Syracuse city should begin with "132".I ran the following query to check for the same:

<code>
sqlite>SELECT tags.value, COUNT(\*) as count 
FROM (SELECT \* FROM node_tags 
      UNION ALL 
      SELECT \* FROM way_tags) tags
WHERE tags.key='postcode'
GROUP BY tags.value
ORDER BY count DESC;
</code>


The dataset has other value codes also that begin with '130' and '131' like the following results.The records for surrounding areas of Syracuse city were also present.

<ul>
<li>13224|821</li>
<li>13214|513</li>
<li>13210|475</li>
<li>13205|282</li>
<li>13206|279</li>
<li>13108|171</li>
<li>13212|136</li>
<li>13057|114</li>
<li>13031|112</li>
<li>13066|110</li>
<li>13104|101</li>
<li>13202|93</li>
<li>13215|78</li>
<li>13204|75</li>
<li>13088|64</li>
<li>13208|50</li>
<li>13203|45</li>
<li>13209|43</li>
<li>13164|40</li>
<li>13219|32</li>
<li>13078|17</li>
<li>13039|16</li>
</ul>

So, I ran another query to sort the cities by count.


#### Sort cities by count in descending order:

<code>
sqlite> SELECT tags.value, COUNT(\*) as count 
FROM (SELECT \* FROM node_tags UNION ALL
      SELECT \* FROM way_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;
</code>

And the results were as follows :

<ul>
<li>Syracuse|2834</li>
<li>DeWitt|808</li>
<li>Marcellus|209</li>
<li>Camillus|158</li>
<li>Fayetteville|116</li>
<li>Manlius|104</li>
<li>North Syracuse|104</li>
<li>East Syracuse|94</li>
<li>Liverpool|69</li>
<li>Solvay|35</li>
<li>Cicero|29</li>
<li>Dewitt|26</li>
<li>Onondaga|25</li>
<li>Jamesville|15</li>
<li>tiger|12</li>
<li>Salina|8</li>
<li>10|5</li>
<li>1|4</li>
<li>Mattydale|4</li>
<li>100|3</li>
<li>2|3</li>
<li>4|3</li>
<li>6|3</li>
<li>8|3</li>
<li>Baldwinsville|3</li>
<li>Nedrow|3</li>
<li>Onondaga Nation|3</li>
<li>12|2</li>
<li>20|2</li>
<li>200|2</li>
<li>39.5 MW|2</li>
<li>80|2</li>
<li>Clay|2</li>
<li>Mattdale|2</li>
<li>1000|1</li>
<li>104|1</li>
<li>109|1</li>
<li>1250|1</li>
<li>13|1</li>
<li>1345|1</li>
<li>170|1</li>
<li>20-30|1</li>
<li>220|1</li>
<li>23|1</li>
<li>280|1</li>
<li>285|1</li>
<li>375|1</li>
<li>425|1</li>
<li>5|1</li>
<li>50|1</li>
<li>520|1</li>
<li>550|1</li>
<li>560|1</li>
<li>575|1</li>
<li>70|1</li>
<li>75|1</li>
<li>77|1</li>
<li>800|1</li>
<li>98|1</li>
<li>Auburn|1</li>
<li>Bridgeport|1</li>
<li>East Syracuse, NY|1</li>
<li>Fulton|1</li>
<li>Kirkville|1</li>
<li>Minoa|1</li>
<li>east Syracuse|1</li>
</ul>


Clearly, the results indicate the presence of surrounding areas of Syracuse City as well, as shown by the postalcodes.

### Data Overview and Additional Ideas:

#### File Sizes :

* Syracuse.osm **...............** 61 MB
* Syracuse.db **................** 35.4 MB
* nodes.csv **..................** 21.9 MB
* node_tags.csv **..............** 1.31 MB
* ways.csv **...................** 1.94 MB
* ways_nodes.csv **.............** 7.40 MB
* ways_tags.csv **..............** 5.71 MB

#### Number of nodes :

<code>
sqlite> SELECT COUNT(\*) FROM nodes;
</code>

278790

#### Number of ways :

<code>
sqlite> SELECT COUNT(\*) FROM way;
</code>

35363

#### Number of unique users :

<code>
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM way) e;
</code>

229

#### Top 10 contributing users :

<code>
sqlite> SELECT e.user, COUNT(\*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM way) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
</code>

* zeromap|158155
* woodpeck_fixbot|75599
* DTHG|27981
* yhahn|8129
* RussNelson|8073
* fx99|4495
* bot-mode|4410
* timr|2859
* TIGERcnl|2077
* Johnc|2035

#### Number of users appearing only once (having 1 post)

<code>
sqlite> SELECT COUNT(\*) 
FROM
    (SELECT e.user, COUNT(\*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM way) e
     GROUP BY e.user
     HAVING num=1)  u;
</code>     

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

<code>
sqlite> SELECT COUNT(DISTINCT tags.value)
FROM (SELECT \* FROM node_tags UNION ALL SELECT \* FROM way_tags) tags
WHERE tags.type = 'source';
</code>
78
#### Top 10 sources of data

<code>
sqlite> SELECT tags.value ,COUNT(\*) as count
FROM (SELECT \* FROM node_tags UNION ALL SELECT \* FROM way_tags) tags
WHERE tags.type='source'
GROUP BY tags.value
ORDER BY count DESC
LIMIT 10;
</code>

* NYSDOT https://www.dot.ny.gov/divisions/operating/oom/transportation-systems/repository/2010%20trk%20access%20bk.pdf | 758
* TIGER 2015 | 576
* survey | 182
* tiger 2015 | 64
* tiger | 24
* National Transportation Atlas Database 2011 | 22
* local knowledge | 19
* Tiger 2015 | 17
* receipt | 12
* JOSM Incomplete Address plugin | 8

### Additional Data Exploration

#### Top 10 appearing amenities

<code>
sqlite> SELECT value, COUNT(*) as num
FROM node_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;
</code>

* school | 152
* bench  |151
* fast_food | 93
* restaurant | 75
* place_of_worship | 73
* post_box | 55
* bicycle_parking | 49
* waste_basket | 37
* pharmacy | 31
* cafe | 30

#### Biggest Religion 

<code>
sqlite> SELECT node_tags.value, COUNT(*) as num
FROM node_tags 
    JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value='place_of_worship') i
    ON node_tags.id=i.id
WHERE node_tags.key='religion'
GROUP BY node_tags.value
ORDER BY num DESC
LIMIT 1;
</code>

* Christian | 69

#### Most Popular Cuisines

<code>
sqlite> SELECT node_tags.value, COUNT(\*) as num
FROM node_tags 
    JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value='restaurant') i
    ON node_tags.id=i.id
WHERE node_tags.key='cuisine'
GROUP BY node_tags.value
ORDER BY num DESC;
</code>

* pizza | 11
* chinese | 8
* american | 7
* italian | 3
* steak_house | 3
* burger | 2
* japanese | 2
* mexican | 2
* sandwich | 2
* Waffles | 1
* diner | 1
* german | 1
* greek  | 1
* hispanic | 1
* indian   | 1
* jamaican | 1
* korean;japanese | 1
* mediterranean  | 1
* seafood | 1
* thai | 1
* vietnamese | 1

#### Number of coffee shops

<code>
sqlite> SELECT node_tags.value, COUNT(\*) as num
FROM node_tags
JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value='cafe') i
ON node_tags.id=i.id
WHERE node_tags.key='amenity'
GROUP BY node_tags.value
ORDER BY num DESC;
</code>

* cafe|30

#### Top 3 coffee shops

<code>
sqlite> SELECT node_tags.value, COUNT(\*) as num
FROM node_tags
JOIN (SELECT DISTINCT(id) FROM node_tags WHERE value LIKE '%cafe%') i
ON node_tags.id=i.id
WHERE node_tags.key='name'
GROUP BY node_tags.value
ORDER BY num DESC;
</code>

* Dunkin Donuts | 8
* Cafe Kubal | 3
* Starbucks | 3

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
