import time
import datetime
import csv
import random
import sys
import urllib2
from subprocess import Popen

#------------------------------------------------------------
#--- Get Interactive Input for number of loops to execute ---
numLoops = int(sys.argv[1])
baseURL = sys.argv[2]
print(str(numLoops)+' '+baseURL)


#--- Read List of PIIs -----------------
PII=[]
try:
	#csvRd = csv.reader(open('/home/ubuntu/PIIs_250k.csv','rb'))
	csvRd = csv.reader(open('/home/ubuntu/PIIS_490.csv','rb'))
except:
	csvRd = csv.reader(open('C:/Scripts/piis-1m.csv','rb'))
for j in csvRd:
        PII.append(j)


idx=0
loop=0
while numLoops > loop:
	Pii=str(PII[idx]).strip('[\']')	
	try:
		print(Pii)
		Popen('phantomjs phantomArticle.js '+baseURL+' '+Pii,shell=True,close_fds=True)
		time.sleep(.5)
	
		loop = loop+1
		idx=idx+1
	except:
		#print('loading browser failed')
		print datetime.datetime.now()
		time.sleep(5)
		pass
