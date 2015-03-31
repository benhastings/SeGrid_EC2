from subprocess import Popen
import sys
import urllib2
import time

script=sys.argv[1]
users=int(sys.argv[2])
duration=float(sys.argv[3])
env=sys.argv[4]
testDurationSecs=str(int(duration*3600))

# # Find hostname to use for passing to webdriver
# resp=urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
# PHOST=resp.read()
# PHOST='localhost'
# inst=urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
# instID=inst.read()
# print(instID)

while users>0:
  #print 'I have entered the loop'
  ex=Popen('python '+script+' '+env+' '+testDurationSecs+'&',shell=True,close_fds=True)
  users=users-1
  time.sleep(10)
	

