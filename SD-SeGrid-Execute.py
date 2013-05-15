from subprocess import Popen
import sys
import urllib2

# Find hostname to use for passing to webdriver
resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
PHOST=resp.read()

# Poll Hub interface to determine free/busy status of resources
try:
	response=urllib2.urlopen('http://localhost:4200/grid/console')
	html=response.read()
	exit
except urllib2.URLError:
	pass

resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
PHOST=resp.read()
	
# If resources available (first condition) add more requests
#   - rename whatever test you want to run to the 'sdtest.py' value
# Otherwise, exit and wait a while
if 'type=WebDriver' in html:
	Popen('python gridExecute.py 10 0 sdtest.py 4000000 '+PHOST+'&',shell=True)
elif 'requests waiting for a slot to be free' in html:
	exit
else:
	exit
