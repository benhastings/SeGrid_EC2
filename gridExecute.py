from subprocess import Popen
import sys

chrome=int(sys.argv[1])
ff=int(sys.argv[2])
script=sys.argv[3]
iterations=sys.argv[4]
hub=sys.argv[5]

processes = []

while ff > 0:
#       processes.append(Popen('python sdTest.py '+iterations+' '+baseURL+' firefox http://'+hub+'/wd/hub', shell=True))
        processes.append(Popen('python sdTest.py '+iterations+' '+baseURL+' firefox '+hub, shell=True))
        ff=ff-1
        print ff

while chrome > 0:
#       processes.append(Popen('python sdTest.py '+iterations+' '+baseURL+' chrome http://'+hub+'/wd/hub', shell=True))
        processes.append(Popen('python '+script+' '+iterations+' chrome '+hub, shell=True, close_fds=True))
        chrome=chrome-1
        print chrome

"""
processes.append(Popen('python C:\Scripts\RC-sdLoad-250kPIIs.py 3 www.sciencedirect.com "internet explorer"', shell=True))
"""

#print('python sdTest.py '+iterations+' '+baseURL+' firefox http://'+hub+'/wd/hub')

for process in processes:
        process.wait()

