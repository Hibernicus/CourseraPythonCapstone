import xml.etree.ElementTree as ET
import urllib2
import sqlite3
import json

tree = ET.parse('geo.xml')
root = tree.getroot()
url_list = list()
lst = list()
url_base = "http://www.parkrun."

## create database
conn = sqlite3.connect('events.sqlite3')
cur = conn.cursor()
cur.executescript('''
DROP TABLE IF EXISTS URLS;
DROP TABLE IF EXISTS Events;

CREATE TABLE URLS (
   id INTEGER NOT NULL PRIMARY KEY UNIQUE,
   domain TEXT
);

CREATE TABLE Events (
   id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
   geodata TEXT,
   domain_ID INTEGER
);    
''')

## read the xml file
for e in root.iter('e'):
   print e.get('n'), e.get('la'), e.get('lo')
   
   myData = '''{
                        "results" : [
                         {
                           "formatted_address" : "''' + e.get('n') + '''", 
                           "geometry" : {
                               "location" : {
                                   "lat" :''' + e.get('la') + ''',
                                   "lng" : ''' + e.get('lo') + '''
                                }
                           }
                         }
                       ],
                       "status" : "OK"
                      }'''
   cur.execute('INSERT OR IGNORE INTO Events (geodata, domain_ID) VALUES ( ? , ?)',
                     (myData, int(e.get('c'))) )
      
## sort ascending domain_IDs to map to corresponding URLs
   if int(e.get('c')) not in lst:
      lst.append(int(e.get('c')))
lst.sort(reverse=False)

## add URLs to list - omit unused URLs
for r in root.iter('r'):
   url = r.get('u')
   if len(url) > 0 and url != "http://www.parkrun.com" and url != "http://www.parkrun.is":
      url_list.append((r.get('n'), url[len(url_base):]))

url_list.sort(reverse=False)

for i in range(len(lst)):
   cur.execute('INSERT OR IGNORE INTO URLS (id, domain) VALUES ( ?,? )',
                     (int(lst[i]), url_list[i][1]))

conn.commit()
cur.close()
conn.close()
