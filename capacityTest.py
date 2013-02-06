from subprocess import Popen
import sys
import time
import datetime

iterations=int(sys.argv[1])
size=sys.argv[2]
hub=sys.argv[3]


browsers=1
while (browsers < iterations):
        print('browsers:'+str(browsers))
        Popen('python gridExecuteCapacity.py '+str(browsers)+' 0 www.sciencedirect.com 5 '+hub+' >> '+size+'-'+str(browsers), shell=True).wait()
        browsers=browsers+1
        if browsers < iterations:
                print(' rest for 60 seconds')
                time.sleep(60)

