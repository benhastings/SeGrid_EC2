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
	# Create array holder for CPU data
	a=[]
	check=1
	while(check >0):
	        fc=0
	        try:
	                response=urllib2.urlopen('http://localhost:4200/grid/console')
	                time.sleep(2)
			html=response.read()
	                exit
	                count = html.count("platform=")
	        	busy = html.count('busy')
	        	wait = html.count('waiting for a slot')
	        
	        	return [count,busy,wait]
	        except urllib2.HTTPError:
	        	#Increment Fail Counter
	        	fc=fc+1
	        	i=5
			while(i>0):
				process = subprocess.Popen('ps -eo pcpu,pid,user,args | grep selenium-server.jar\ \-role', shell=True, stdout=subprocess.PIPE)
				a.append(float(process.communicate()[0].split()[0]))
				i=i-1
				time.sleep(5)
	        	if fc > 6:
	        		check = 0
	        	time.sleep(30)


        
	#return busy

freeCount=freeCheck()
print 'count:'+str(freeCount[0])
print 'busy:'+str(freeCount[1])

# Check CPU 
#process = subprocess.Popen('ps -eo pcpu,pid,user,args | sort -k 1 -r | head -10', shell=True, stdout=subprocess.PIPE)

def mean(numberList):
    if len(numberList) == 0:
        return float('nan')
 
    floatNums = [float(x) for x in numberList]
    return sum(floatNums) / len(numberList)

mean(a)
