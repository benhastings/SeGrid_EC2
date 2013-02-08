from subprocess import Popen
import sys
import time
import datetime

iterations=int(sys.argv[1])
loop=int(sys.argv[2])
size=sys.argv[3]
hub=sys.argv[4]

iter=0
while (iter < loop):
	browsers=1
        while (browsers < iterations):
                print('browsers:'+str(browsers))
                #Popen('python gridExecuteCapacity.py '+str(browsers)+' 0 www.sciencedirect.com 5 '+hub+' >> '+size+'-'+str(browsers), shell=True).wait()
                #Popen('python gridExecuteCapacity.py '+str(browsers)+' 0 cdc311-www.sciencedirect.com 5 '+hub+' '+size+' >> '+size, shell=True).wait()
                Popen('python gridExecuteCapacity.py '+str(browsers)+' 0 www.sciencedirect.com 15 '+hub+' '+size+' >> InstanceCapTest', shell=True).wait()
                browsers=browsers+1
                if browsers < iterations:
                        print(' rest for 10 seconds')
                        time.sleep(10)
        iter=iter+1
        time.sleep(300)

