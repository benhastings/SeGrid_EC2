#import subprocess
from subprocess import Popen, PIPE
import sys
import urllib2
import time
import csv
import random

hostNm=sys.argv[1]
duration=int(sys.argv[2])
renderArticles=sys.argv[3]
"""
PII=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/PIIs_250k.csv','rb'))
	piiCount = 250000
except:
	csvRd = csv.reader(open('C:/Scripts/piis-1m.csv','rb'))
	piiCount = 1000000
for j in csvRd:
        PII.append(j)
"""
PII=['S0023643896900377','S2095254614000271','S2095254614000337','S0966636213001173','S2095254614000313']
piiCount=5


#Define end of test based on input above
endTime = int(time.time()+duration)
endTime = int(time.time()+30)

#while loops>0:
while endTime > int(time.time()):

	idx = int(random.random()*piiCount)
	idxPii=idx
	#print('articleIDX:'+str(idx))
	inputPII=str(PII[idxPii]).strip('[\']')
	#print(inputPII)
	#print 'I am trying the phantomJS request now'
	#ex=Popen('phantomjs article.js '+hostNm+' '+inputPII+' '+renderArticles,stdout=PIPE)#,close_fds=True,shell=True)
	ex=Popen(['phantomjs', 'article.js',hostNm,inputPII,renderArticles],stdout=PIPE)#,close_fds=True,shell=True)
	exOut=ex.communicate()
	#print('ex.communicate below:')
	#print(exOut)
	#print(exOut[0])
	try:
		print(inputPII+' '+exOut[0][exOut[0].index(':')+1:])
	except:
		print('something wrong with article')
		print(inputPII+' '+exOut[0])
	time.sleep(.25)

	
