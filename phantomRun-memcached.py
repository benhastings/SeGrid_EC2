#import subprocess
from subprocess import Popen, PIPE
import sys
import urllib2
import time
import csv
import random
import socket

env=sys.argv[1]
duration=int(sys.argv[2])
#statsDHost='ec2-54-80-6-76.compute-1.amazonaws.com'
statsDHost='statsd.elsst.com'

"""
  Input Data collection/Definition
"""

PII=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/piis.csv','rb'))
	piiCount = 500000
except:
	csvRd = csv.reader(open('C:/Scripts/piis-1m.csv','rb'))
	piiCount = 1000000
for j in csvRd:
        PII.append(j)
"""
PII=['S0023643896900377','S2095254614000271','S2095254614000337','S0966636213001173','S2095254614000313']
piiCount=5
"""

"""
  Define UDP connection to send data to statsD
"""
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
## statsd host & port
addr=(statsDHost,8125)



#Define end of test based on input above
endTime = int(time.time()+duration)
#endTime = int(time.time()+30)

if env.find('sdfe') > -1:
  envPrint=env[:env.find('sdfe')]


elif env.find('cdc')> -1:
  envPrint=env[:env.find('-www')]
else:
  envPrint='prod'

#print envPrint

#while loops>0:
while endTime > int(time.time()):
   l=[]
   loop=5
   while loop>0:
	idx = int(random.random()*piiCount)
	idxPii=idx
	#print('articleIDX:'+str(idx))
	inputPII0=str(PII[idxPii]).strip('[\']')
	inputPII1=str(PII[idxPii+1]).strip('[\']')
	inputPII2=str(PII[idxPii+2]).strip('[\']')
	inputPII3=str(PII[idxPii+3]).strip('[\']')
	inputPII4=str(PII[idxPii+4]).strip('[\']')
	#inputPII='S0008874905000535'
	#print(inputPII0+' '+inputPII1+' '+inputPII2)
	#print 'I am trying the phantomJS request now'
	#ex=Popen('phantomjs article.js '+hostNm+' '+inputPII+' '+renderArticles,stdout=PIPE)#,close_fds=True,shell=True)
	count='sd.article.phantom.'+envPrint+'.total:5|c'
	l.append(count+'\n')
	
	ex=Popen(['phantomjs', 'articleCrawl.js',env,inputPII0,inputPII1,inputPII2,inputPII3,inputPII4],stdout=PIPE)#,close_fds=True,shell=True)
	exOut=ex.communicate()
	#print('ex.communicate below:')
	#print(exOut)
	#print(exOut[0])
	#print(inputPII)
	
	time.sleep(.25)
        
	loop=loop-1
   	# statsDdata=''.join(l)
   	# print(statsDdata)
   	# UDPSock.sendto(statsDdata,addr)
        tmStmp=time.time()
        with open("articleCount.log", "a") as myfile:
          myfile.write(str(tmStmp)+'|'+count+'\n')
   	#print(count)
   	UDPSock.sendto(count,addr)
