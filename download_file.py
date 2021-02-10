import urllib2

headers = { 'User-Agent' : 'Mozilla/5.0' }

url = "http://www.parkrun.org.uk/wp-content/themes/parkrun/xml/geo.xml"
xml_file = urllib2.urlopen(urllib2.Request(url, None, headers))
   
with open('geo.xml','wb') as output:
  output.write(xml_file.read())
