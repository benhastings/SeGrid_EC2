from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import random
import sys
import urllib2
#from pyvirtualdisplay import Display

#--- Start Virtual Display -------------------
#display = Display(visible=1, size=(1280, 800))
#display.start()

#--- Browser definition for Grid usage ----------

browser = sys.argv[3]

#--- Get Interactive Input for number of loops to execute ---
numLoops = int(sys.argv[1])

baseURL = sys.argv[2]
hub = sys.argv[4]


#--- Read List of PIIs -----------------
PII=[]
csvRd = csv.reader(open('SDFE-Piis-41k.csv','rb'))
for j in csvRd:
        PII.append(j)


#---------------------------------------
#       Function to gracefully exit the browser
#               after incrementing loop variables
#-----------
def egress():
        try:
                driver.quit()
        #except WindowsError:
        #        print ("****WindowsError - pass? ****")
        #        pass
        except urllib2.URLError:
                print ("----URLError - pass? ----")
                pass


#------------------------------------------------------
#       Function to execute a request or page interaction
#               handles associated error conditions
#               Makes call to collect page timing
#-------------
def getPage(resource):
	try:
		#driver.get("http://"+baseURL)
		resource
		if 'Unable to process' in driver.title:
			print 'Error - Unable to process, wait 60 seconds'
			time.sleep(60)
			pass
		elif 'Error' in driver.title:
			print 'Error, wait 60 seconds'
			time.sleep(60)
			pass
		else:
			#if 'SD Content Delivery' in titl:
			if 'article' in titl:
				metricsCollect(titl,Pii)
			else:
				metricsCollect(titl,'NA')
			time.sleep(.25)
	except urllib2.URLError:
		print 'URLError'
		pass
	except:
		print (titl+' fail')
		pass


#-------------------------------------------------------
#       Function to capture various page timing metrics
#               and output to screen for log tailing and troubleshooting
#---------------

#def metricsCollect(dtitl,PII,sections):
def metricsCollect(dtitl,ID):
	try:
		navS = driver.execute_script("return performance.timing.navigationStart")
		#print(navS)
		respS = driver.execute_script("return performance.timing.responseStart")
		respE = driver.execute_script("return performance.timing.responseEnd")
		dom = driver.execute_script("return performance.timing.domInteractive")
		loadE = driver.execute_script("return performance.timing.loadEventEnd")
		domC = str(driver.execute_script("return document.getElementsByTagName('*').length"))
		if loadE > navS:
			pgLoad = str(int(loadE-navS))
			domI = str(int(dom-navS))
			cont = str(int(respE-navS))
			ttfb = str(int(respS-navS))
			#print('\nperf details found\n')
		else:
			pgLoad = 'NA'
			domI='NA'
			cont='NA'
			ttfb = 'NA'
			#print('perf details NOT found')



		# Datetime for Timestamp
		dt = datetime.datetime.now()
		dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))

		if 'SD Content Delivery' in dtitl:
			print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+ID)
		else:
			print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+dtitl+'\t'+ID)
	except:
		if 'Pii' in globals():
			print('Unable to print perfTiming details, PII:'+Pii)
		else:
			print('Unable to print perfTiming details')
		try:
			driver.quit()
		#except WindowsError:
		#       print ("******WindowsError - pass? ****")
		#       pass
		except urllib2.URLError:
			print ("------URLError - pass? ----")
			pass

        #
        # End metricsCollect()
        #


#=============================================================
#-------------------------------------------------------------
#       Script Begins Here
#-------------------------------------------------------------
#=============================================================

#--- Define static Article Value for looping
idx=0

while numLoops > 0:
        
	#print('iteration: '+str(numLoops)+' browser:'+browser)
	"""
	Define capabilities of remote webdriver
			Specifically: assign browser type
	"""
	#driver=webdriver.Chrome()
	
	driver=webdriver.Remote(
			"http://"+hub+":4200/wd/hub",

			desired_capabilities={
				"browserName": browser,
				
			}	

	)
	

	time.sleep(.25)

	#-------------------------------------------------
	#       View Article(s) with scrolling where possible
	#               View multiple articles in same session 33%
	#-------------------------------------------------
	artLoop = 5
	"""	
        if (login%3==0):
                artLoop=8
        if (login%3==1):
                artLoop=4
        else:
                artLoop=2
	"""
	#print ('artLoop: '+str(artLoop))
	loop = 0
	while artLoop >= loop:
			#--- Define Random Value ---------------
			idx = int(random.random()*41000)
			idxPii=idx
			Pii=str(PII[idxPii]).strip('[\']')
			testBase=['article1','article2','article2a','article3','article4']
			for test in testBase:
				titl=test
				try:
					if (loop == 0):
						#print('try to get: '+"http://"+baseURL+"/science/article/pii/"+Pii)
						#http://sdfe:Els3vier@sdfe.atsonaws.com/article1/S0140673606685875
						getPage(driver.get("http://sdfe:Els3vier@"+baseURL+"/"+test+"/"+Pii))
						#print(str(loop)+'\t'+str(artLoop)+'\t'+Pii+'\t'+test+'\t'+titl)
					else:
						getPage(driver.get("http://"+baseURL+"/"+test+"/"+Pii))
						#print(str(loop)+'\t'+str(artLoop)+'\t'+Pii+'\t'+test+'\t'+titl)
				except urllib2.URLError:
						pass
				time.sleep(1)
			
			if artLoop >= loop:
					loop = loop+1
					idx = idx+1
	

	numLoops = numLoops-1
	idx=idx+1
	egress()
