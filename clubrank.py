import sqlite3

conn = sqlite3.connect('results.sqlite3')
cur = conn.cursor()
events = dict()
def get_sec(s):
    l = s.split(':')
    return float(int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2]))/50

cur.execute('''SELECT club_ID, COUNT(*) AS `num` FROM
                Fastest GROUP BY club_ID''')

for row in cur:
    club_id = row[0]
    club_count = row[1]
    sor = conn.cursor()
    sor.execute('''UPDATE Clubs SET club_count = ?
            WHERE ID = ?''', (club_count, club_id))
conn.commit()

cur.execute('''SELECT * FROM Clubs JOIN Fastest
                ON Fastest.club_ID = Clubs.id WHERE Clubs.id != 0''')

for row in cur:
    club_id = row[0]
    seconds = get_sec(row[7])
    print seconds
    sor = conn.cursor()
    sor.execute('UPDATE Clubs SET club_average = club_average + ? WHERE id = ?', (seconds, club_id))   
conn.commit()
    
cur.execute('SELECT id, club_count, club_average FROM Clubs')
for row in cur:
    sor = conn.cursor()
    club_id = row[0]
    mean = row[2]/row[1]
    sor.execute('''UPDATE Clubs SET club_average = ? WHERE id = ?''', (mean, club_id))
    print club_id, mean

cur.execute('SELECT id FROM Clubs')
for row in cur:
    lst = list()
    club_id = row[0]
    sor = conn.cursor()
    sor.execute('SELECT club_id, event_id FROM Fastest WHERE club_id = ?', (club_id,))
    for item in sor:
        if(item[1]) in lst: continue
        lst.append(item[1])
        events[club_id] = lst
        
for item in events:
    club_id = item
    div = float(len(events[item]))
    div = div/20.0 + 1.0
    print club_id, div
    cur.execute('SELECT club_average FROM Clubs WHERE id = ?', (club_id,))
    div = div *200/(cur.fetchone()[0])
    cur.execute('UPDATE Clubs SET club_rate = ? WHERE id = ?', (div, club_id))
conn.commit()
conn.close()

    

