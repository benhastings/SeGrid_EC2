#import subprocess
from subprocess import Popen, PIPE
import sys
import urllib2
import time
import csv
import random
import socket

hostNm=sys.argv[1]
duration=int(sys.argv[2])
renderArticles=sys.argv[3]
env=sys.argv[4]
statsDHost='ec2-54-80-6-76.compute-1.amazonaws.com'


"""
  Input Data collection/Definition
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

#while loops>0:
while endTime > int(time.time()):
   l=[]
   loop=5
   while loop>0:
	idx = int(random.random()*piiCount)
	idxPii=idx
	#print('articleIDX:'+str(idx))
	inputPII=str(PII[idxPii]).strip('[\']')
	#print(inputPII)
	#print 'I am trying the phantomJS request now'
	#ex=Popen('phantomjs article.js '+hostNm+' '+inputPII+' '+renderArticles,stdout=PIPE)#,close_fds=True,shell=True)
	l.append('sd.article.phantom.'+env+'.total:1|c\n')
	ex=Popen(['phantomjs', 'article.js',hostNm,inputPII,renderArticles,env],stdout=PIPE)#,close_fds=True,shell=True)
	exOut=ex.communicate()
	#print('ex.communicate below:')
	#print(exOut)
	#print(exOut[0])
	#print(inputPII)
	try:
		#print('find duration')
		ms=exOut[0][exOut[0].index(':')+1:exOut[0].index('ms')]
		#print(inputPII+' '+ms)
		#print('add timer to statsD')
		l.append('sd.article.phantom.'+env+':'+ms+'|ms\n')
		#print('add counter to statsD')
		l.append('sd.article.phantom.'+env+'.pass:1|c\n')
	except:
		print('something wrong with article: '+inputPII+' '+exOut[0])
		try:
		  if exOut[0].index('Error'):
		    l.append('sd.article.phantom.'+env+'.fail:1|c\n')
		except:
		  pass
	time.sleep(.25)
        
	loop=loop-1
   statsDdata=''.join(l)
   #print(statsDdata)
   UDPSock.sendto(statsDdata,addr)
