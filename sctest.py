from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import csv
import random
import sys
import urllib2

#--- Get Interactive Input ------------
#-- Number of iterations to execute----
numLoops = int(sys.argv[1])

#-- base domain of website to test-----
#baseURL = sys.argv[2]

#-- Desired browser -------------------
browser = sys.argv[2]

#-- SeGrid Hub hostname ---------------
hub = sys.argv[3]


#--- Read List of PIIs -----------------
scTerms = []
try:
    scSrch = csv.reader(open('C:/Scripts/ScopusSearchTerms.csv', 'rb'))
except:
    scSrch = csv.reader(open('/home/ubuntu/ScopusSearchTerms.csv', 'rb'))
for r in scSrch:
    scTerms.append(r)


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
    except:
        print ("--- Other Error on Exit -----")
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
        #print(driver.title)
        if 'Unable to process' in driver.title:
            print 'Error - Unable to process, wait 60 seconds'
            time.sleep(60)
            pass
        elif 'Server Busy' in driver.title:
            print 'Server Busy, wait 2 seconds'
            time.sleep(2)
        elif 'Error' in driver.title:
            print 'Error, wait 60 seconds'
            time.sleep(60)
            pass
        elif 'Page Not Found' in driver.title:
            print 'Error, wait 60 seconds'
            time.sleep(60)
            pass
        elif 'Welcome' in driver.title:
            try:
                #print('trying login')
                try:
                    time.sleep(3)
                    driver.find_element_by_id('loginPlus').click()
                    time.sleep(3)
                    driver.find_element_by_id('username').send_keys('Webmetrics')
                    driver.find_element_by_id('password').send_keys('Scidir_test')
                    time.sleep(3)
                    driver.find_element_by_xpath('//input[@title="Login"]').click()
                except:
                    driver.get('https://'+baseURL+'/customer/authenticate/loginfull.url')
                    time.sleep(3)
                    driver.find_element_by_id('loginFormUsername').send_keys('Webmetrics')
                    driver.find_element_by_id('loginFormPassword').send_keys('Scidir_test')
                    time.sleep(3)
                    driver.find_element_by_xpath('//input[@title="Login"]').click()
                    time.sleep(10)
                    pass
            except:
                #print('login failed')
                pass
        else:
            metricsCollect(titl, 'NA')
            time.sleep(.25)
    except urllib2.URLError:
        print 'URLError'
        pass
    except:
        print (titl + ' fail')
        pass

#-------------------------------------------------------
#       Function to capture various page timing metrics
#               and output to screen for log tailing and troubleshooting
#---------------

#def metricsCollect(dtitl,PII,sections):
def metricsCollect(dtitl, ID):
    #print ('dtitl:'+dtitl+' ID:'+ID)
    try:
        navS = driver.execute_script("return performance.timing.navigationStart")
        #print(navS)
        respS = driver.execute_script("return performance.timing.responseStart")
        respE = driver.execute_script("return performance.timing.responseEnd")
        dom = driver.execute_script("return performance.timing.domInteractive")
        loadE = driver.execute_script("return performance.timing.loadEventEnd")
        domC = str(driver.execute_script("return document.getElementsByTagName('*').length"))
        if loadE > navS:
            pgLoad = str(int(loadE - navS))
            domI = str(int(dom - navS))
            cont = str(int(respE - navS))
            ttfb = str(int(respS - navS))
        #print('\nperf details found\n')
        else:
            pgLoad = 'NA'
            domI = 'NA'
            cont = 'NA'
            ttfb = 'NA'
        #print('perf details NOT found')



        # Datetime for Timestamp
        dt = datetime.datetime.now()
        dTm = str(dt.strftime("%Y/%m/%d %H:%M:%S%Z"))

        if 'SD Content Delivery' in dtitl:
        #       if sections > 0:
        #               print(browser+'\t'+dTm+'\t'+pgLoad+'\t'+domI+'\t'+cont+'\t'+ttfb+'\t'+domC+'\t'+PII+'\t'+sections)
        #       else:
            print(
            browser + '\t' + dTm + '\t' + pgLoad + '\t' + domI + '\t' + cont + '\t' + ttfb + '\t' + domC + '\t' + ID)
        else:
            print(
            browser + '\t' + dTm + '\t' + pgLoad + '\t' + domI + '\t' + cont + '\t' + ttfb + '\t' + domC + '\t' + dtitl)
    except:
        if 'Pii' in globals():
            print('Unable to print perfTiming details, PII:' + Pii)
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


while numLoops > 0:
#       print('user:'+user+' iteration: '+str(numLoops)+' browser:'+browser)
    pdName = 'SC'
    # Datetime for Timestamp
    dt = datetime.datetime.now()
    dTm = dt.strftime("%Y%m%d_%H%M_%S%Z")
    #----------------------------
    #	Initialize Index & System
    #---------
    idx = int(random.random() * 19110)

    if (idx % 3 == 0):
        baseURL = 'cdc311-www.scopus.com'
    elif (idx % 3 == 1):
        baseURL = 'cdc314-www.scopus.com'
    elif (idx % 3 == 2):
        baseURL = 'cdc318-www.scopus.com'
    baseURL = 'cdc329-www.scopus.com'

    #----------------------------
    #	Initialize Browser
    #---------

    #driver = webdriver.Chrome()
    #--- For Grid execution ------
    driver=webdriver.Remote("http://"+hub+":4200/wd/hub",desired_capabilities={"browserName": browser})

    time.sleep(.25)

    #-----------------------------
    #	Begin Script Execution
    #---------
    #--- Request Home Page ----------------------------------------
    titl = 'Home Page'
    getPage(driver.get("http://" + baseURL))
    time.sleep(.25)
    #--- Find Login Form & Fill in data ---------------------------
    if 'Document Search' in driver.title: #find_elements_by_xpath('//input[@title="Search"]'):
        pass
    elif 'Choose Organization' in driver.title: #find_elements_by_xpath('//input[@name="path_choice"]'):
        try:
            driver.find_elements_by_xpath('//input[@type="radio"]')[0].click()
            time.sleep(.5)
            try:
                continueButton = driver.find_elements_by_xpath('//input[@title="Continue with path choice"]')
                print('button Found')
                try:
                    print('attempt button click')
                    getPage(continueButton.click())
                    time.sleep(5)
                except:
                    print('attempt JS button click')
                    jsBtn = 'clickButton(' + continueButton + ');'
                    getPage(driver.execute_script(jsBtn))
                    time.sleep(5)
                """
                finally:
                    print('button click fail')
                    #break
                """
            except:
                print('button NOT Found')
                exit

            #getPage(continueButton.click())
            time.sleep(2.25)
        except:
            pass
    # Start Loop through search, etc...
    for i in range(0, idx % 10):
        #print('i is:' + str(i))
        #if ['Server Busy','Welcome'] not in driver.title:
        #if 'Server Busy.' != driver.title:
        if driver.title.find('Server Busy') < 1:
            #print(driver.title.find('Server Busy'))
            #print('server NOT busy')

            #-----------------------------
            #  Search
            #---------
            if (i > 1):
                try:
                    getPage(driver.get("http://" + baseURL))
                    driver.find_element_by_id('searchterm1').clear()
                except:
                    pass


            #	Enter Terms
            try:
                #print('enter search terms')
                driver.find_element_by_id('searchterm1').send_keys(str(scTerms[idx + i]))
                time.sleep(.25)
            except:
                pass
                #	Submit Search
            #print 'Search Submit'
            titl = 'Basic Search'
            try:
                """
                try:
                        print ('xpath 1')
                        driver.find_elements_by_xpath('//input[@title="Search"]')[1]
                except:
                        print ('xpath 1 failed')
                        pass
                try:
                        print ('xpath 2')
                        driver.find_elements_by_xpath('//input[@title="Search"]')[0]
                except:
                        print ('xpath 2 failed')
                        pass
                try:
                        print ('xpath 3')
                        driver.find_elements_by_xpath('//input[@value="Search"]')[1]
                except:
                        print ('xpath 3 failed')
                        pass
                """
                #print('submit search')
                getPage(driver.find_elements_by_xpath('//input[@title="Search"]')[0].click())

                time.sleep(.25)

            except:
                print('search submit failed')
                pass


            #-------------------------------------
            #  Select first Record 40% of the time
            #---------

            if (i % 10 < 4):
                titl = 'Record Page'
                try:
                    getPage(driver.find_element_by_xpath("//a[contains(@href, '/record/')]").click())
                    time.sleep(.25)
                except:
                    pass

            #-------------------------------------
            #  Select Author Profile 40% of the time
            #---------
            if (i % 10 > 4):
                titl = 'Author Profile'
                try:
                    getPage(driver.find_element_by_xpath("//a[contains(@href,'authorId=')]").click())
                    time.sleep(.25)
                except:
                    pass
        else:
            print('Something failed')
            pass

    numLoops = numLoops - 1
    egress()

