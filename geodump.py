import sqlite3
import json
import codecs
import re

conn = sqlite3.connect('events.sqlite3')
cur = conn.cursor()
sor = conn.cursor()

cur.execute('SELECT * FROM Events ')
fhand = codecs.open('where_parkrun.js','w', "utf-8")
fhand.write("myData = [\n")
count = 0

for row in cur :
    data = str(row[1])
    domain_ID = str(row[2])
    
    try:
        js = json.loads(str(data))
        
    except: continue

    if not('status' in js and js['status'] == 'OK') : continue
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0 : continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")

    sor.execute('''SELECT * FROM URLS JOIN Events
                ON URLS.id = Events.domain_ID WHERE URLS.id ==''' + domain_ID + '''''')
    url = sor.fetchone()[1]
    
    try :
        print where, lat, lng
        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"', '"+url+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print count, "records written to where.js"
print "Open where_parkrun.html to view the data in a browser"

