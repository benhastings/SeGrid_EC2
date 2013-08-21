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


#------------------------------------------------------------
#--- Get Interactive Input for number of loops to execute ---
numLoops = int(sys.argv[1])

#--- Browser definition for Grid usage ----------
browser = sys.argv[2]

#--- SeGrid Hub designation --------------------
hub = sys.argv[3]

baseURL='hothouse.atsonaws.com/loadTest/form'

#--- Read List of Search Terms -----------------
SRCH=[]
#csvRd = csv.reader(open('/opt/SeResources/SDSrchTerms.csv','rb'))
#csvRd = csv.reader(open('C:/Scripts/SDSrchTerms.csv','rb'))
try:
        text_file = open("/home/ubuntu/labs_queries.txt", "r")
except:
        text_file = open("C:/Scripts/labs_queries.txt", "r")

csvRd = text_file.readlines()
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
#       Function to execute a request or page interaction
#               handles associated error conditions
#               Makes call to collect page timing
#-------------
def getPage(resource):
	try:
		#driver.get("http://"+baseURL)
		resource
		time.sleep(.01)
		if 'Load Test Search Results' in driver.title:
			metricsCollect(titl,'NA')
			time.sleep(.01)
		elif 'Error' in driver.title:
			print 'Error, redirect to search Form'
			driver.get("http://sdfe:Els3vier@"+baseURL)
			time.sleep(1)
			pass
		else:
			#metricsCollect(titl,'NA')
			time.sleep(.05)
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
                #       if sections > 0:
                #               print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+PII+'\t'+sections)
                #       else:
                        print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+ID)
                else:
                        print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+dtitl)
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
	idx=int(random.random()*350000)
	srIDX = idx%349999

	print('iteration: '+str(numLoops)+' browser:'+browser)
	"""
	Define capabilities of remote webdriver
			Specifically: assign browser type
	
	# Standalone Usage
	"""
	#driver=webdriver.Chrome()

	# Webdriver Usage with SeGrid
	try:	
		driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities={"browserName": browser})
	
		time.sleep(.01)
	
		#-------------------------------------------------
		#       Find Search form then submit search
		#-------------------------------------------------
		try:
			titl='Search Form'
			getPage(driver.get("http://sdfe:Els3vier@"+baseURL))
			time.sleep(.01)
			assert "Load Test Search Form" in driver.title
	
			try:
				sr = 50
				while (sr > 0):
					srIDX = idx%349999
					print('idx:'+str(idx))#+' srch:'+SRCH[srIDX])
					try:
						#print('find box by id')
						srchBox = driver.find_element_by_id("quickSearch")
						#print('found by id')
					except:
						#print('find box by xpath')
						srchBox = driver.find_element_by_xpath("//input[contains(@name,'quickSearch')]")
						#print('found by xpath')
					finally:
						pass
	
					#print('enter search terms')
					titl='Search'
					getPage(srchBox.send_keys(SRCH[srIDX]))
					time.sleep(.01)
					#--- Submit Form --------
					#titl='Search'
					#getPage(driver.find_element_by_xpath("//input[contains(@value,'Submit')]").click())
					#print('click submit button')
					#driver.find_element_by_xpath("//input[contains(@value,'Submit')]").click()
					#time.sleep(10)
					#metricsCollect(titl,'NA')
	
	
	
					idx=idx+1								
					sr=sr-1
	
			except:
				print 'Search failed'
				pass
	
		except:
			'Search form not found'
	#except if browser doesn't open
	except:
		pass
	numLoops = numLoops-1
	idx=idx+1
	egress()
