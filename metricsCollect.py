def metricsCollect(dtitl,d,base):
		l=''
		# print(dtitl+' - trying metricsCollect')
		try:
			# print('try some script execute')

			navS = d.execute_script("return performance.timing.navigationStart")
			# print('navS: '+str(navS)+' '+dtitl)
			respS = d.execute_script("return performance.timing.responseStart")
			respE = d.execute_script("return performance.timing.responseEnd")
			dom = d.execute_script("return performance.timing.domInteractive")
			loadE = d.execute_script("return performance.timing.loadEventEnd")
			domCLoad = d.execute_script("return performance.timing.domContentLoadedEventEnd")
			# print('core metrics collected')
			if loadE > navS:
				pgLoad = str(int(loadE-navS))
				domI = str(int(dom-navS))
				domCL = str(int(domCLoad-navS))
				cont = str(int(respE-navS))
				ttfb = str(int(respS-navS))

				# print('\nperf details found\n')
				l+='sd.Selenium.'+base+'.'+dtitl+'.ttfb:'+ttfb+'|ms\n'
				l+='sd.Selenium.'+base+'.'+dtitl+'.pgl:'+pgLoad+'|ms\n'
				l+='sd.Selenium.'+base+'.'+dtitl+'.pgi:'+domI+'|ms\n'
				l+='sd.Selenium.'+base+'.'+dtitl+'.domcl:'+domCL+'|ms\n'
				l+='sd.Selenium.'+base+'.'+dtitl+'.html:'+cont+'|ms\n'
				# print(ttfb+'\t'+domCL+' '+base+' '+dtitl)
			
				if (dtitl.find('Content') != -1):
					try:
						# print('try article PCR')
						try:
							# print('try return prs.abs_end')
							pcrT=d.execute_script("return prs.abs_end")
						except:
							# print("try return prs['abs_end']")
							pcrT=d.execute_script("return prs['abs_end']")
						# prs=d.execute_script('return prs')
						# pcrT=prs['abs_end']
						
					except:
						pcrT=0
						# print('could not get article PCR')
						pass
				elif (dtitl.find('Category_Home') != -1):
					prs=d.execute_script('return prs')
					prsT=[]
					prsT.append(prs['pcr'])
					prsT.append(prs['pcr_nav'])
					pcrT=sorted(prsT)[1]
				else:
					pcrT=d.execute_script("return prs.pcr")
				if pcrT > navS:
					pcr = str(int(pcrT-navS))
					l+='sd.Selenium.'+base+'.'+dtitl+'.pcr:'+pcr+'|ms\n'

                return l
