import sqlite3
import urllib
import zlib
import re

count = 0
fhand = open('gword.js','w')
fhand.write("gword = [")
conn = sqlite3.connect('results.sqlite3')
cur = conn.cursor()
name = ""
cur.execute('''SELECT  club, club_rate FROM Clubs ORDER BY club_rate DESC''')
first = True
for row in cur:
    if row[0] == "Unaffiliated": continue
    if count == 101:
        break
    count+=1
    line = row[0].split()
    if len(line) > 1:
        if line[1] == "and" or line[1] == "of" or line[1] == "&":
            name = str(line[0]+line[2])
        else:
            name = str(line[0]+line[1])
    else:
        name = line[0]
    
    size = int(row[1])+3
##    if len(name) == 0:continue
##    print name
##    if name == "Unaffiliated":
##        size = size/5
    ##size = int(size/2)
    if not first : fhand.write( ",\n")
    first = False
    print name, size
    fhand.write("{text: '"+name +"', size: "+str(size)+"}")
    name = ""
fhand.write( "\n];\n")
cur.close

print "Output written to gword.js"
print "Open gword.htm in a browser to view"
