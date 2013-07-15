from subprocess import Popen
import sys
import urllib2
import time
# Find hostname to use for passing to webdriver
resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
PHOST=resp.read()

# Poll Hub interface to determine free/busy status of resources
def freeCheck():
	try:
        	response=urllib2.urlopen('http://localhost:4200/grid/console')
        	html=response.read()
        	exit
	except urllib2.URLError:
        	pass

	count = html.count("platform=")
	return count

# If resources available (first condition) add more requests
#   - rename whatever test you want to run to the 'sdtest.py' value
# Otherwise, exit and wait a while
#if 'type=WebDriver' in html:
freeCount=freeCheck()
if freeCount > 0:
	idx=freeCount
	while (idx > 0):
		#Popen('python gridExecute.py ' + str(freeCount) + ' 0 sdtest.py 4000000 '+PHOST+'&',shell=True)
        	Popen('python gridExecute.py 4 0 sdtest.py 4000000 '+PHOST+'&',shell=True)
		time.sleep(10)
		freeCount=freeCheck()
		if freeCount>0:
			idx = freeCount-4
			time.sleep(30)
		else:
			exit		

elif 'requests waiting for a slot to be free' in html:
        exit
else:
        exit
