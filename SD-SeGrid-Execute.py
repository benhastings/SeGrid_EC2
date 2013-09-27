from subprocess import Popen
import sys
import urllib2
import time
# Find hostname to use for passing to webdriver
resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
PHOST=resp.read()
PHOST='localhost'

# Poll Hub interface to determine free/busy status of resources
def freeCheck():
        try:
                response=urllib2.urlopen('http://localhost:4200/grid/console')
                time.sleep(2)
		html=response.read()
		count = html.count("platform=")
                #exit
        except urllib2.URLError:
                count = 0
        except urllib2.HTTPError:
                count = 0
                pass

        return count

# If resources available (first condition) add more requests
#   - rename whatever test you want to run to the 'sdtest.py' value
# Otherwise, exit and wait a while
#if 'type=WebDriver' in html:
freeCount=0
freeCount=freeCheck()
while freeCount>1:
        Popen('python gridExecute.py 2 0 sdtest.py 400 '+PHOST+'&',shell=True,close_fds=True)
	try:
		url2Send = urllib2.urlopen('http://cert-pa.elsevier.com/perfTest?perfTest.cpc=SD&perfTest.cpc.newScripts=2')        
        except:
		pass
	time.sleep(30)
        try:
                freeCount=freeCheck()
		time.sleep(2)
                #print('fc:'+str(freeCount))
        except:
                freeCount=0
		exit




		
