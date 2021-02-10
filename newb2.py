from bs4 import BeautifulSoup
import urllib2
import sys


headers = { 'User-Agent' : 'Mozilla/5.0' }

webstring = "/gateshead/results/fastest500/"
url = "http://www.parkrun.org.uk"+webstring

try:
   orig_stdout = sys.stdout
   f = file('fast_500.txt', 'w')
   sys.stdout = f

   html = urllib2.urlopen(urllib2.Request(url, None, headers)).read()
   soup = BeautifulSoup(html, "html.parser")
   results_table = soup.find("table", {'id': "results"})
   table_rows = results_table.find_all("tr")
   th = results_table.find_all('th')
   for item in th:
      print item.text,
   print '\n'
   for i in range(26):
      td = table_rows[i].find_all("td") 
      count = 0
      
      for item in td:
         
         try:
            u_string = str(item.text)
         except:
            u_string = "Not Affiliated"

         if td.index(item) % 4 == 0 or td.index(item) % 5 == 0:
            print u_string
         count+=1
      if count == 6:
         print '\n'
         count = 0
      
   
   sys.stdout = orig_stdout
   f.close()
except:
   print (sys.exc_info()[0])         

