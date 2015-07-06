from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import random
import sys
import urllib2
import socket

# from metricsCollect import metricsCollect

#------------------------------------------------------------
#--- Get Interactive Input for number of loops to execute ---
#numLoops = int(sys.argv[1])
timeToRun=int(sys.argv[1])
endTime=int(time.time()+timeToRun)

#--- SeGrid Hub designation --------------------
hub = 'localhost'


stats=''
#statsDHost='ec2-54-80-6-76.compute-1.amazonaws.com'
statsDHost='statsd.elsst.com'
"""
  Define UDP connection to send data to statsD
"""
UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
## statsd host & port
addr=(statsDHost,8125)


#--- Read List of PIIs -----------------
PII=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/PIIs_250k.csv','rb'))
	#csvRd = csv.reader(open('/home/ubuntu/PIIs_30k.csv','rb'))
	piiCount = 29000
except:
	csvRd = csv.reader(open('./PIIs_250k.csv','rb'))
	piiCount = 29000
for j in csvRd:
        PII.append(j)


#--- Read List of Journals -----------------
JRNL=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/Journals.csv','rb'))
except:
	csvRd = csv.reader(open('./Journals.csv','rb'))
for j in csvRd:
        JRNL.append(j)

#--- Read List of Search Terms -----------------
SRCH=[]
try:
	csvRd = csv.reader(open('/home/ubuntu/SDSrchTerms.csv','rb'))
except:	
	csvRd = csv.reader(open('./SDSrchTerms.csv','rb'))
for j in csvRd:
        SRCH.append(j)

#---------------------------------------
#       Function to gracefully exit the browser
#               after incrementing loop variables
#-----------
def egress():
	try:
		driver.quit()
		# except WindowsError:
		# 	print ("****WindowsError - pass? ****")
		# 	pass
	except urllib2.URLError:
		# print ("----URLError - pass? ----")
		pass

#------------------------------------------------------
# Function to send error details for tracking
#------------------------------------------------------
def errorReport(hName,titlN,msg):
	# l.append('sd.Selenium.error.'+base+'.'+titlN+':1|c\n')
	try:
	 	stats
		stats+='sd.Selenium.error.'+base+'.'+titlN+':1|c\n'
	except:
		stats='sd.Selenium.error.'+base+'.'+titlN+':1|c\n'
	try:
	  print('error - '+msg+' '+titlN+' '+driver.title)
	except:
	  print('error - '+msg+' '+titlN)

#------------------------------------------------------
# Function to send error details for tracking
#------------------------------------------------------
def newBrowser(base):
	# l.append('sd.Selenium.'+base+'.newBrowser:1|c\n')
	stats+='sd.Selenium.'+base+'.newBrowser:1|c\n'

	print('new Browser - '+base)

#------------------------------------------------------
# collect metrics to pass into statsD/influxDB
#------------------------------------------------------
def metricsCollect(dtitl,d):#,baseIn):
    print('in metricsCollect')
    l=[]
    l.append('sd.Selenium.'+base+'.'+titl+'.pass:1|c\n')
    metrics={'ttfb':'responseStart','html':'responseEnd','pgi':'domInteractive','pgl':'loadEventEnd','startRender':'domContentLoadedEventEnd'}
    try:
        navS = d.execute_script('return performance.timing.navigationStart')
        for i in metrics:
            compVal=int(d.execute_script('return performance.timing.'+metrics[i])-navS)
            if(compVal>0):
                l.append('sd.Selenium.'+base+'.'+dtitl+'.'+str(i)+':'+str(compVal)+'|ms\n')

        try:
            prsT=[]
            prs=d.execute_script('return prs')
            try:
                prsT.append(prs['pcr'])
            except:
                pass
            try:
                prsT.append(prs['pcr_nav'])
                l.append('sd.Selenium.'+base+'.'+dtitl+'.pcr_nav:'+str(int(prs['pcr_nav']-navS))+'|ms\n')
            except:
                pass
            try:
                prsT.append(prs['abs_end'])
            except:
                pass
            pcrT=sorted(prsT)[len(prsT)-1]
        except:
            pcrT=0
        if pcrT > navS:
            l.append('sd.Selenium.'+base+'.'+dtitl+'.pcr:'+str(int(pcrT-navS))+'|ms\n')

        for i in prs:
            if str(i).find('scr_')>-1:
                print i
                l.append('sd.Selenium.'+base+'.'+dtitl+'.'+i+':'+str(int(prs[i]-navS))+'|ms\n')
    except:
        pass

    # print('l is:')
    # print(l)
    # print 'join statsDdata'
    statsDdata=''.join(l)
    # print('here is statsDdata')
    print(statsDdata)

    try:
      print('try to send UDP message')
      print UDPSock.sendto(statsDdata,addr)
    
    except:
      print('UDP send failed')
      pass
    d.execute_script("SDM.ep.prDeviceTemp=SDM.ep.prDevice")
    d.execute_script("SDM.ep.prDevice='http://rumserver-479135682.us-west-2.elb.amazonaws.com'")
    d.execute_script("SDPA.sendPage()")
    # d.execute_script("SDPA.sendIndex()")
    d.execute_script("SDPA.pcrSend()")
    d.execute_script("SDM.ep.prDevice=SDM.ep.prDeviceTemp")
    time.sleep(.25)


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
			# print 'Error - Unable to process, wait 60 seconds'
			errorReport(base,titl,'Unable to Process')
			time.sleep(60)
			exit
		elif 'ScienceDirect Error' in driver.title:
			dt = datetime.datetime.now()
                	dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))
			# print 'SD-00x Error'+dTm
			errorReport(base,titl,'SD-00x')
			time.sleep(1)
			exit
		elif 'Error' in driver.title:
			# print 'Error, wait 60 seconds'
			time.sleep(10)
			exit
		else:
			# l.append('sd.Selenium.'+base+'.'+titl+'.pass:1|c\n')
			time.sleep(.5)
			print('trying metricsCollect')
			try:
				print('try to append to stats')
				# testHolder=metricsCollect(titl,driver,base)
				metricsCollect(titl,driver)
				# UDPSock.sendto(testHolder,addr)
				# print(testHolder)
				# stats +=''.join(testHolder)
				# print(stats)
			except:
				# print('no append to stats, create instead')
				# stats=''.join(metricsCollect(titl,driver,base))			
				pass
				
	except urllib2.URLError:
		# print 'URLError'
		errorReport(base,titl,'URLError')
		pass
	except:
		# print (titl+' fail')
		errorReport(base,titl,'Other')
		pass


#=============================================================
#-------------------------------------------------------------
#       Script Begins Here
#-------------------------------------------------------------
#=============================================================
#--- Define static Article Value for looping
idx=0
while endTime > time.time():
	"""
	Define capabilities of remote webdriver
			Specifically: assign browser type
	"""
	
	try:
		# stats=''
		# print('loading browser')
		#driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities={"browserName": browser})
		#driver=webdriver.Chrome()
		options=webdriver.ChromeOptions()
        	options.add_argument('--disable-logging')
        	driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities=options.to_capabilities())	
		# print('wait for it...')	
		# print datetime.datetime.now()
		time.sleep(.25)
	
		# Initialize array for holding metrics to send to graphite
		# l = []
		

		#-------------------------------------------------
		#       Define baseURL for following transactions
		#-------------------------------------------------
		baseIDX=int(random.random()*300)
		
		if (baseIDX%3==0):
			baseURL = 'cdc311-www.sciencedirect.com'
			base='cdc311'
		if (baseIDX%3==1):
			baseURL = 'cdc314-www.sciencedirect.com'
			base='cdc314'
		if (baseIDX%3==2):
			baseURL = 'cdc318-www.sciencedirect.com'
			base='cdc318'

		# baseURL = 'cdc318-www.sciencedirect.com'
		# base='cdc318'

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
				driver.find_element_by_name("arrow").click()
	
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
			# print ('artLoop: '+str(artLoop))
			
			#Comment out for sequential evaluation of articles
			#idx = int(random.random()*499000)
			
			
			while artLoop > 0:
				#--- Define Random Value ---------------
				idx = int(random.random()*piiCount)
				idxPii=idx
				# print('articleIDX:'+str(idx))
				Pii=str(PII[idxPii]).strip('[\']')
				titl = 'Content_Delivery'
				#sStart = time.time()
				try:
					print('try to get: '+"http://"+baseURL+"/science/article/pii/"+Pii)
					getPage(driver.get("http://"+baseURL+"/science/article/pii/"+Pii))
				except urllib2.URLError:
					time.sleep(.25)	
					pass
				
				try:
					dtitl=driver.title[:50]
					print(dtitl[:50])
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
					if (artLoop%5 < 2):
					# if (artLoop%5 < 6):
						titl='Search_Results'
						SrIdx = int(random.random()*100)%100
						# print('trying search')	

						srString=str(SRCH[SrIdx]).strip('[\']').decode('string_escape')
						# print srString
						try:
							dtitl=driver.title#[:50]
							# print 'dtitl: '+dtitl
							# Article Page Search
							s=driver.find_element_by_css_selector('input#quickSearch')
							s.send_keys(srString)
							getPage(driver.find_element_by_css_selector('input.submit').click())

							# # Other Pages					
							# s=d.find_element_by_id("qs_all")
							# >>> s.send_keys('berries')
							# >>> d.find_element_by_id("submit_search").click()

						except:
							# print ('Search form not found '+baseURL)
							time.sleep(.5)
							pass
					#if (login%6 > 4):
					if (artLoop%5 > 2):
						#--- Load Browse List - "Category List" -------------
						titl='Category_List'
						# print('trying browse')	
						getPage(driver.get("http://"+baseURL+"/science/journals"))
	
						#--- Load Journal Home Pages - "Category Home" ------
						jrnLoop = 2
						while jrnLoop > 0:
							titl='Category_Home'
							idx=idx+jrnLoop
							jIdx=idx%120
							# print('trying journal')	
							getPage(driver.get("http://"+baseURL+"/science/journal/"+str(JRNL[jIdx]).strip('[\']')))
							jrnLoop=jrnLoop-1
				except:
					egress()
					exit
					
				if artLoop > 0:
					artLoop = artLoop-1
					idx = idx+1
	
			browserLoop=browserLoop-1
			# print(browserLoop)
		
			# print 'join statsDdata'	
			# statsDdata=''.join(l)
			# print('here is statsDdata')
			print(stats)
			#UDPSock.sendto(statsDdata,addr)
			# l=[]
			stats=''
		loop = loop+1
		idx=idx+1
		egress()
	except:
		if(len(stats) > 0):
			#statsDdata=''.join(l)
			# print('here is statsDdata')
			print(stats)
			
			#UDPSock.sendto(statsDdata,addr)

		# print('loading browser failed')
		# print time.time()
		# print titl
		errorReport(base,titl,'Start Browser Fail')
		#print(statsDdata)
		time.sleep(5)
		pass
