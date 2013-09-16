from subprocess import Popen
import sys
import urllib2
import time
# Find hostname to use for passing to webdriver
resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
PHOST=resp.read()
#PHOST='localhost'

# Poll Hub interface to determine free/busy status of resources
def freeCheck():
        try:
                response=urllib2.urlopen('http://localhost:4200/grid/console')
                html=response.read()
                exit
        except urllib2.URLError:
                pass

        free = html.count("platform=")
        tot = html.count("chrome.png")
        count = tot-free
        return count

# If resources available (first condition) add more requests
#   - rename whatever test you want to run to the 'sdtest.py' value
# Otherwise, exit and wait a while
#if 'type=WebDriver' in html:
freeCount=freeCheck()
while freeCount>0:
        if (freeCount > 5):
                Popen('python gridExecute.py 5 0 sdtest.py 40000 '+PHOST+'&',shell=True,close_fds=True)
        elif (freeCount > 2):
                Popen('python gridExecute.py 2 0 sdtest.py 40000 '+PHOST+'&',shell=True,close_fds=True)
        else:
                Popen('python gridExecute.py 1 0 sdtest.py 40000 '+PHOST+'&',shell=True,close_fds=True)
        
        time.sleep(60)
        try:
                freeCount=freeCheck()
                #print('fc:'+str(freeCount))
        except:
                exit
