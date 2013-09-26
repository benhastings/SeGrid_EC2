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
                exit
        except urllib2.URLError:
                pass

        count = html.count("platform=")
        busy = html.count('busy')
        
        return [count,busy]
	#return busy

# If resources available (first condition) add more requests
#   - rename whatever test you want to run to the 'sdtest.py' value
# Otherwise, exit and wait a while
#if 'type=WebDriver' in html:
freeCount=freeCheck()
print 'count:'+str(freeCount[0])
print 'busy:'+str(freeCount[1])



"""
while freeCount>0:
        #Popen('python gridExecute.py 2 0 sdtest.py 40000 '+PHOST+'&',shell=True,close_fds=True)
	#url2Send = urllib2.urlopen('http://cert-pa.elsevier.com/perfTest?perfTest.cpc=SD&perfTest.cpc.newScripts=2')        
        time.sleep(30)
        try:
                freeCount=freeCheck()
		time.sleep(2)
                #print('fc:'+str(freeCount))
        except:
                exit

"""


		
