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
import socket


#------------------------------------------------------------
#--- Get Interactive Input for number of loops to execute ---
numLoops = int(sys.argv[1])

#--- Browser definition for Grid usage ----------
browser = sys.argv[2]

#--- SeGrid Hub designation --------------------
hub = sys.argv[3]

instID = sys.argv[4]

base=''
titl=''
statsDHost='ec2-54-80-6-76.compute-1.amazonaws.com'
"""
  Define UDP connection to send data to statsD
"""
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
## statsd host & port
addr=(statsDHost,8125)



#--- Read List of PIIs -----------------
PII=[]
try:
	#csvRd = csv.reader(open('/home/ubuntu/PIIs_250k.csv','rb'))
	csvRd = csv.reader(open('/home/ubuntu/PIIs_30k.csv','rb'))
	piiCount = 29000
except:
	csvRd = csv.reader(open('C:/Scripts/piis-1m.csv','rb'))
	piiCount = 29000
for j in csvRd:
        PII.append(j)


#--- Read List of Journals -----------------
JRNL=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/Journals.csv','rb'))
except:
	csvRd = csv.reader(open('C:/Scripts/Journals.csv','rb'))
for j in csvRd:
        JRNL.append(j)

#--- Read List of Search Terms -----------------
SRCH=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/SDSrchTerms.csv','rb'))
except:	
	csvRd = csv.reader(open('C:/Scripts/SDSrchTerms.csv','rb'))
for j in csvRd:
        SRCH.append(j)

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
# Function to send error details for tracking
#------------------------------------------------------
def errorReport(hName,titlN,msg):
	sendBack='http://cert-pa.elsevier.com/perfTest?perfTest.error.cpc=SD&perfTest.error.cpc.host='+hName+'&perfTest.error.cpc.host.page='+titl+'&perfTest.error.cpc.host.page.msg='+msg
	try:
		url2Send = urllib2.urlopen(sendBack)        
		#print('error url sent')
	except:
		#print('error url NOT sent')
		pass
	
#------------------------------------------------------
# Function to send error details for tracking
#------------------------------------------------------
def newBrowser(base):
	sendBack='http://cert-pa.elsevier.com/perfTest?perfTest.cpc=SD&perfTest.cpc.'+base+'.newBrowser=1&perfTest.cpc.'+base+'.id='+instID
	try:
		url2Send = urllib2.urlopen(sendBack)        
		#print('error url sent')
	except:
		#print('error url NOT sent')
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
			errorReport(base,titl,'Unable to Process')
			time.sleep(10)
			exit
		elif 'ScienceDirect Error' in driver.title:
			dt = datetime.datetime.now()
                	dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))
			print 'SD-00x Error'+dTm
			errorReport(base,titl,'SD-00x')
			time.sleep(1)
			exit
		elif 'Error' in driver.title:
			print 'Error, wait 60 seconds'
			time.sleep(10)
			exit
		else:
			l.append('sd.Selenium.'+base+'.'+titl+'.pass:1|c\n')
			metricsCollect(titl)
			"""
			if 'SD Content Delivery' in titl:
				time.sleep(1)
				pass
			else:
				pass
			"""			
			time.sleep(.25)
                
	except urllib2.URLError:
		print 'URLError'
		errorReport(base,titl,'URLError')
		pass
	except:
		print (titl+' fail')
		errorReport(base,titl,'Other')
		pass


#-------------------------------------------------------
#       Function to capture various page timing metrics
#               and output to screen for log tailing and troubleshooting
#---------------

#def metricsCollect(dtitl,PII,sections):
def metricsCollect(dtitl):
        try:
                navS = driver.execute_script("return performance.timing.navigationStart")
                #print(navS)
                respS = driver.execute_script("return performance.timing.responseStart")
                respE = driver.execute_script("return performance.timing.responseEnd")
                dom = driver.execute_script("return performance.timing.domInteractive")
                loadE = driver.execute_script("return performance.timing.loadEventEnd")
                domCLoad = driver.execute_script("return performance.timing.domContentLoadedEventEnd")
                domC = str(driver.execute_script("return document.getElementsByTagName('*').length"))
                if loadE > navS:
                        pgLoad = str(int(loadE-navS))
                        domI = str(int(dom-navS))
                        domCL = str(int(domCLoad-navS))
                        cont = str(int(respE-navS))
                        ttfb = str(int(respS-navS))
                        #print('\nperf details found\n')
                        l.append('sd.Selenium.'+base+'.'+titl+'.ttfb:'+ttfb+'|ms\n')
                        l.append('sd.Selenium.'+base+'.'+titl+'.pgl:'+pgLoad+'|ms\n')
                        l.append('sd.Selenium.'+base+'.'+titl+'.pgi:'+domI+'|ms\n')
                        l.append('sd.Selenium.'+base+'.'+titl+'.domcl:'+domCL+'|ms\n')
                        l.append('sd.Selenium.'+base+'.'+titl+'.html:'+cont+'|ms\n')
    
                
        except:
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
loop=1
while numLoops > loop:
	#print('iteration: '+str(loop)+' browser:'+browser)
	"""
	Define capabilities of remote webdriver
			Specifically: assign browser type
	"""
	
	try:
		#print('loading browser')
		driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities={"browserName": browser})
		#driver=webdriver.Chrome()
		#print('wait for it...')	
		#print datetime.datetime.now()
		time.sleep(.25)
	
		#-------------------------------------------------
		#       Define baseURL for following transactions
		#-------------------------------------------------
		baseIDX=int(random.random()*300)
		"""
		if (baseIDX%4==0):
			baseURL = 'cdc311-www.sciencedirect.com'
			base='cdc311'
		if (baseIDX%4==1):
			baseURL = 'cdc323-www.sciencedirect.com'
			base='cdc323'
		if (baseIDX%4==2):
			baseURL = 'cdc318-www.sciencedirect.com'
			base='cdc318'
		if (baseIDX%4==3):
			baseURL = 'cdc314-www.sciencedirect.com'
			base='cdc314'
		"""
		"""
		if (baseIDX%3==0):
			baseURL = 'cdc311-www.sciencedirect.com'
			base='cdc311'
		if (baseIDX%3==1):
			baseURL = 'cdc314-www.sciencedirect.com'
			base='cdc314'
		if (baseIDX%3==2):
			baseURL = 'cdc323-www.sciencedirect.com'
			base='cdc323'
		"""
		if (baseIDX%2==0):
			baseURL = 'cdc311-www.sciencedirect.com'
			base='cdc311'
		if (baseIDX%2==1):
			baseURL = 'cdc314-www.sciencedirect.com'
			base='cdc314'
		try:
			newBrowser(base)
		except:
			pass
		#-------------------------------------------------
		#       Load Home Page & Authenticate x% of iterations
		#-------------------------------------------------
		login = int(random.random()*100)
		if (login%100 < 50):
			#--- Request Home Page ----------------------------------------
			titl='Home_Page'
			getPage(driver.get("http://"+baseURL))
	
			#--- Find Login Form & Fill in data ---------------------------
			try:
				driver.find_element_by_id("loginPlusScript").click()
				driver.find_element_by_id('username').send_keys('Webmetrics')
				driver.find_element_by_id('password').send_keys('Scidir_test')
	
	
				#--- Submit the form based on element ID ----------------
				titl='U/P Auth to Home Page'
				getPage(driver.find_element_by_name("arrow").click())
	
				#--- If choose Org screen displayed, select appropriate value
				if 'Choose Organization' in driver.title:
					titl='Choose Org to Home Page'
					try:
						driver.find_element_by_id('1').click()
						driver.find_element_by_class_name('button').click()
						#metricsCollect(titl)
					except:
						pass
			except:
					egress()
					exit
	
	
		#-------------------------------------------------
		#      Add looping structure to minimize browser churn
		#-------------------------------------------------
		l=[]
		browserLoop=4				
		while(browserLoop > 0):
			#-------------------------------------------------
			#       View Article(s) with scrolling where possible
			#               View multiple articles in same session 33%
			#-------------------------------------------------
			artLoop = 5
			"""
			if (login%3==0):
					artLoop=8
			else:
					artLoop=4
			"""
			#print ('artLoop: '+str(artLoop))
			
			#Comment out for sequential evaluation of articles
			#idx = int(random.random()*499000)
			
			
			while artLoop > 0:
				#--- Define Random Value ---------------
				idx = int(random.random()*piiCount)
				idxPii=idx
				#print('articleIDX:'+str(idx))
				Pii=str(PII[idxPii]).strip('[\']')
				titl = 'Content_Delivery'
				#sStart = time.time()
				try:
					#print('try to get: '+"http://"+baseURL+"/science/article/pii/"+Pii)
					getPage(driver.get("http://"+baseURL+"/science/article/pii/"+Pii))
				except urllib2.URLError:
					time.sleep(.25)	
					pass
				
				try:
					dtitl=driver.title[:50]
					#print(dtitl[:50])
				except:
					egress()
					exit
				"""	
				if artLoop > 0:
					artLoop = artLoop-1
					idx = idx+1
				"""
	
				try:
					#if (login%6 == 0):
					if (artLoop%5 == 1):
						titl='Search'
						SrIdx = int(random.random()*100)%100
						#print('trying search')	
						try:
							inputElement = driver.find_element_by_id("quickSearch")
							#print('search element found')
							inputElement.send_keys(SRCH[SrIdx])
							#print('search text entered')
							time.sleep(.10)
							#--- Submit Form --------
							getPage(driver.find_element_by_xpath("//button[contains(@title,'Submit quick search')]").click())
						except:
							print ('Search form not found '+baseURL)
							pass
					#if (login%6 > 4):
					if (artLoop%5 == 3):
						#--- Load Browse List - "Category List" -------------
						titl='Browse_List'
						#print('trying browse')	
						getPage(driver.get("http://"+baseURL+"/science/browse"))
	
						#--- Load Journal Home Pages - "Category Home" ------
						jrnLoop = 2
						while jrnLoop > 0:
							titl='Journal_Home'
							idx=idx+jrnLoop
							jIdx=idx%2500
							#print('trying journal')	
							getPage(driver.get("http://"+baseURL+"/science/journal/"+str(JRNL[jIdx]).strip('[\']')))
							jrnLoop=jrnLoop-1
				except:
					egress()
					exit
					
				if artLoop > 0:
					artLoop = artLoop-1
					idx = idx+1
	
			browserLoop=browserLoop-1
			#print(browserLoop)
			statsDdata=''.join(l)
			print(statsDdata)
			UDPSock.sendto(statsDdata,addr)
		loop = loop+1
		idx=idx+1
		egress()
	except:
		#print('loading browser failed')
		print datetime.datetime.now()
		errorReport(base,titl,'Start Browser Fail')
		time.sleep(5)
		pass