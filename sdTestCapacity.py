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
from pyvirtualdisplay import Display

#--- Start Virtual Display -------------------
#display = Display(visible=1, size=(1280, 800))
#display.start()

#--- Browser definition for Grid usage ----------

browser = sys.argv[3]

#--- Get Interactive Input for number of loops to execute ---
numLoops = int(sys.argv[1])

baseURL = sys.argv[2]
hub = sys.argv[4]
count = sys.argv[5]
size = sys.argv[6]

#--- Read List of PIIs -----------------
PII=[]
csvRd = csv.reader(open('PIIs_250k.csv','rb'))
for j in csvRd:
        PII.append(j)


#--- Read List of Journals -----------------
JRNL=[]
csvRd = csv.reader(open('Journals.csv','rb'))
for j in csvRd:
        JRNL.append(j)

#--- Read List of Search Terms -----------------
SRCH=[]
csvRd = csv.reader(open('SDSrchTerms.csv','rb'))
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

                if 'SD Content Delivery' in dtitl:
                #       if sections > 0:
                #               print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+PII+'\t'+sections)
                #       else:
                        print(size+'\t'+count+'\t'+browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+ID)
                else:
                        print(size+'\t'+count+'\t'+browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+dtitl)
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
        driver=webdriver.Remote(
                "http://"+hub+":4200/wd/hub",

                desired_capabilities={
                        "browserName": browser
                }

                #desired_capabilities.chrome()
        )


        time.sleep(.25)


        #-------------------------------------------------
        #       Load Home Page & Authenticate x% of iterations
        #-------------------------------------------------
        login = int(random.random()*100)
        if (login%100 < 100):
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
                """
		if 'ScienceDirect.com' in dtitl:
                        titl='SD Content Delivery'
                        time.sleep(.25)
                        try:
                                secs=driver.find_elements_by_class_name("svArticle")
                                #print 'Sections:'+str(len(secs))
                                if len(secs) > 0 and numLoops%2 > 0:
                                        if len(secs) > 2:
                                                #print 'scroll to 1'
                                                driver.execute_script("arguments[0].scrollIntoView();",secs[1])
                                                time.sleep(.75)
                                        if len(secs) > 10:
                                                #print 'scroll to 9'
                                                driver.execute_script("arguments[0].scrollIntoView();",secs[9])
                                                time.sleep(.75)
                                        if len(secs) > 30:
                                                #print 'scroll to 29'
                                                driver.execute_script("arguments[0].scrollIntoView();",secs[29])
                                                time.sleep(.75)
                                        if len(secs) > 70:
                                                #print 'scroll to 69'
                                                driver.execute_script("arguments[0].scrollIntoView();",secs[69])
                                                time.sleep(.75)


                                try:
                                        refs = driver.find_element_by_class_name("references")
                                        scStart = time.time()
                                        #print 'scroll to References'
                                        driver.execute_script("arguments[0].scrollIntoView();",refs)
                                        try:
                                                wait.until(lambda driver: driver.find_elements_by_partial_link_text('Cited By in Scopus ('))
                                        except: # end waiting for references to resolve
                                                pass
                                except: # end try scrolling to references
                                        pass
                        except: # end try scrolling
                                pass


                elif 'Article Locator' in dtitl:
                        titl='ALP'
                        pass
                else:
                        titl='Other'
                        pass
		"""
                #secStr=str(len(secs))
                #metricsCollect(titl,Pii,secStr)
                if artLoop > 0:
                        artLoop = artLoop-1
                        idx = idx+1
        
	"""
	try:
                if ('ScienceDirect.com' in driver.title):
                        #if (login%6 == 0):
                        if (login%6 < 3):
                      		titl='Search'
                                SrIdx = int(random.random()*100)%100

                                try:
                                	inputElement = driver.find_element_by_id("quickSearch")
                                        #print('search element found')
                                        inputElement.send_keys(SRCH[SrIdx])
                                        #print('search text entered')
                                        time.sleep(.5)
                                        #--- Submit Form --------
                                        getPage(driver.find_element_by_xpath("//button[contains(@title,'Submit quick search')]").click())
                                except:
                                        print 'Search form not found'
                                        pass
                        
			#if (login%6 > 4):
                        if (login%6 > 3):
                                #--- Load Browse List - "Category List" -------------
                                titl='Category List'
                                getPage(driver.get("http://"+baseURL+"/science/browse"))

                                #--- Load Journal Home Pages - "Category Home" ------
                                jrnLoop = 2
                                while jrnLoop > 0:
                                        titl='Category Home'
                                        idx=idx+jrnLoop
                                        jIdx=idx%2500
                                        getPage(driver.get("http://"+baseURL+"/science/journal/"+str(JRNL[jIdx]).strip('[\']')))
                                        jrnLoop=jrnLoop-1
			
        except:
                pass


	"""
        numLoops = numLoops-1
        idx=idx+1
        egress()

#--- Stop Virtual Display ------------
#display.stop()
                                    

