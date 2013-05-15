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



#--- Read List of PIIs -----------------
PII=[]
csvRd = csv.reader(open('/opt/SeResources/piis-1m.csv','rb'))
for j in csvRd:
        PII.append(j)


#--- Read List of Journals -----------------
JRNL=[]
csvRd = csv.reader(open('/opt/SeResources/Journals.csv','rb'))
for j in csvRd:
        JRNL.append(j)

#--- Read List of Search Terms -----------------
SRCH=[]
csvRd = csv.reader(open('/opt/SeResources/SDSrchTerms.csv','rb'))
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
                if 'Unable to process' in driver.title:
                        print 'Error - Unable to process, wait 60 seconds'
                        time.sleep(60)
                        pass
                elif 'Error' in driver.title:
                        print 'Error, wait 60 seconds'
                        time.sleep(60)
                        pass
                else:
                        if 'SD Content Delivery' in titl:
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
                """
                if 'SD Content Delivery' in dtitl:
                #       if sections > 0:
                #               print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+PII+'\t'+sections)
                #       else:
                        print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+ID)
                else:
                        print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+dtitl)
                """
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
        print('iteration: '+str(numLoops)+' browser:'+browser)
        """
        Define capabilities of remote webdriver
                Specifically: assign browser type
        """
        driver=webdriver.Remote(
                "http://"+hub+":4200/wd/hub",

                desired_capabilities={
                        "browserName": browser
                }

                #desired_capabilities.chrome()
        )

        time.sleep(.25)

  #-------------------------------------------------
        #       Define baseURL for following transactions
        #-------------------------------------------------
	baseIDX=int(random.random()*300)
	if (baseIDX%2==0):
		baseURL = 'cdc311-www.sciencedirect.com'
	if (baseIDX%2==1):
		baseURL = 'cdc323-www.sciencedirect.com'

	print(baseURL)		
        #-------------------------------------------------
        #       Load Home Page & Authenticate x% of iterations
        #-------------------------------------------------
        login = int(random.random()*100)
        if (login%100 < 75):
                #--- Request Home Page ----------------------------------------
                titl='Home Page'
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
                        pass




        #-------------------------------------------------
        #       View Article(s) with scrolling where possible
        #               View multiple articles in same session 33%
        #-------------------------------------------------
        artLoop = 1
        if (login%3==0):
                artLoop=8
        else:
                artLoop=2

        #print ('artLoop: '+str(artLoop))

		idx = int(random.random()*250000)
        while artLoop > 0:
                #--- Define Random Value ---------------
                #idx = int(random.random()*250000)
                idxPii=idx
                Pii=str(PII[idxPii]).strip('[\']')
                titl = 'SD Content Delivery'
                #sStart = time.time()
                try:
                        #print('try to get: '+"http://"+baseURL+"/science/article/pii/"+Pii)
                        getPage(driver.get("http://"+baseURL+"/science/article/pii/"+Pii))
                except urllib2.URLError:
                        pass
                time.sleep(.25)
                try:
                        dtitl=driver.title[:50]
                        #print(dtitl[:50])
                except:
                        egress(numLoops,idx)
                
	
                if artLoop > 0:
                        artLoop = artLoop-1
                        idx = idx+1

        numLoops = numLoops-1
        idx=idx+1
        egress()