import sqlite3

fastest = dict()
clubs = list()
conn = sqlite3.connect('results.sqlite3')
cur = conn.cursor()

cur.execute('''SELECT * FROM Clubs JOIN Fastest
             ON Fastest.club_id=Clubs.id WHERE Clubs.id != 0
             ORDER BY speed''')
def get_sec(s):
    l = s.split(':')
    return str(l[1]+"." +l[2][0]) 

count = 0
compte = 0
longest = 0
for row in cur:
    club = row[1]
    compte = 0
    if count == 18:
        break
    sor = conn.cursor()
    sor.execute('''SELECT * FROM Clubs JOIN Fastest
                 ON Fastest.club_id=Clubs.id WHERE Clubs.club = ?
                 ORDER BY speed''', (club, ))
    lst = list()
    current_club = None
    current_speed = None
    for line in sor:
        current_club = line[1]
        current_speed = line[7]
        if compte == (len(line)-1) or compte == 11: 
            break
        if current_speed in lst: continue
        lst.append(get_sec(current_speed))
        compte += 1
    
    fastest[current_club] = lst
    if longest < len(lst):
        longest = len(lst)
    count += 1
#print longest


for club in fastest:
    new_list = fastest[club]
    while len(new_list) < longest:
        new_list.append("'null'")
    fastest[club] = new_list
    #print fastest[club]

scores = dict()


for i in range(longest):
    times = list()
    indx = str(i+1)
    if len(indx) == 1:
        indx = "-0" + indx
    elif len(indx) == 2:
        indx = "-" + indx
    times.append(indx)
    for club in fastest:
        times.append(fastest[club][i])
        scores[i] = times
#print scores

scores_list = list()

for sc in scores:
    scores_list.append((scores[sc][0], scores[sc][1:]))

##for sl in scores_list:
##    print sl
    
fhand = open('pline.js','w')
fhand.write("pline = [ ['Position'")
for club in fastest:
    fhand.write(",'"+str(club)+"'")
fhand.write("]")
                
for sl in scores_list:
    fhand.write(",\n['"+ sl[0] +"'")
    for t in sl[1]:
        fhand.write(","+str(t))
    fhand.write("]");
fhand.write("\n];\n")

print "Data written to pline.js"
print "Open gline.htm in a browser to view"
cur.close()
