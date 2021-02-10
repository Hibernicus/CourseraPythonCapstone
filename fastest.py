from bs4 import BeautifulSoup
import urllib2
import sqlite3
import json
import sys


headers = { 'User-Agent' : 'Mozilla/5.0' }
results = None
base_url = "http://www.parkrun."
## create database
conn = sqlite3.connect('results.sqlite3')
cur = conn.cursor()
cur.executescript('''

CREATE TABLE IF NOT EXISTS Fastest (
     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
     event_ID INTEGER,
     speed TIME,
     club_ID INTEGER
);

CREATE TABLE IF NOT EXISTS Clubs (
     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
     club TEXT UNIQUE,
     club_count INTEGER,
     club_rate FLOAT,
     club_average FLOAT
);
''')
### NOTE - COLUMN 'CLUB_AVERAGE' ADDED TO Clubs TABLE
### IN SQL BROWSER BEFORE RUNNING 'clubrank.py"


nect  = sqlite3.connect('events.sqlite3')
sor = nect.cursor()
sor.execute('''SELECT * FROM URLS JOIN Events
                ON Events.domain_ID = URLS.id WHERE URLS.id != 0''')

noc = nect.cursor()
noc.execute('''SELECT * FROM Events''')

def fastest_25(event, domain):
    event_ID = noc.fetchone()[0]
    if domain == "pl":
        results = "/rezultaty/najszybszych500/"
    else:
        results = "/results/fastest500/"

    url = base_url + domain + "/" + event + results
    
    try:
        html = urllib2.urlopen(urllib2.Request(url, None, headers)).read()
        soup = BeautifulSoup(html, "html.parser")
        results_table = soup.find("table", {'id': "results"})
        table_rows = results_table.find_all("tr")
        for i in range(26):
           lst = list()
           td = table_rows[i].find_all("td")
           for item in td:
               
               try:
                   u_string = str(item.text)
                   lst.append(u_string)
               except:
                   u_string = "Unaffiliated"
                   lst.append(u_string)
                
               if len(lst)>5:
                   print lst[4],lst[5]
                   count = 0
                   rate= 0
                   cur.execute('INSERT OR IGNORE INTO Clubs(club, club_count, club_rate) VALUES ( ? , ? , ? )',
                               (lst[5], count, rate))
                   cur.execute('SELECT id FROM Clubs WHERE club = ? ', (lst[5], ))
                   club_ID = cur.fetchone()[0]
                   cur.execute('SELECT club_count FROM Clubs')
                   cur.execute('INSERT INTO Fastest(event_ID, speed, club_ID) VALUES ( ?, ?, ?)',
                               (event_ID,lst[4], club_ID))
        conn.commit()           
        
    except:
        print (sys.exc_info())
    return

for row in sor:
    try:
        data = str(row[3])
        js = json.loads(str(data))
        if not ('status' in js and js['status'] == 'OK') : continue
        e_vent = js['results'][0]['formatted_address']
        e_vent = e_vent.replace("'","")
        fastest_25(e_vent, row[1])
            
    except:
        print (sys.exc_info())

conn.close()
nect.close()
