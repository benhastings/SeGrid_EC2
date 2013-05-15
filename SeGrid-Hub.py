from subprocess import Popen
import sys
import urllib2

html=''
#-- Check to see if SeGrid Hub is available
try:
	response=urllib2.urlopen('http://localhost:4200/grid/console')
	html=response.read()
	exit
except urllib2.URLError:
	pass

#-- If SeGrid Hub available, move on, if not, start it
if 'Grid Hub' in html:
	exit
else:
	Popen('java -Xmx512m -jar /home/ubuntu/selenium-server.jar -role hub -port 4200 -DPOOL_MAX=256 -timeout 300 -browserTimeout 60 -cleanUpCycle 900000&',shell=True)

