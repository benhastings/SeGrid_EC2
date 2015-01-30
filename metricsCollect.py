def metricsCollect(dtitl,d,base):
	l=''
	# metrics=['responseStart','responseEnd','domInteractive','loadEventEnd','domContentLoadedEventEnd']
	metrics={'ttfb':'responseStart','html':'responseEnd','pgi':'domInteractive','pgl':'loadEventEnd','startRender':'domContentLoadedEventEnd'}
	# print(dtitl+' - trying metricsCollect')
	try:
		# print('try some script execute')
		navS = d.execute_script('return performance.timing.navigationStart')
		# print('navS: '+str(navS))
		# print('try getting other metrics')
		for i in metrics:
			compVal=int(d.execute_script('return performance.timing.'+metrics[i])-navS)
			if(compVal>0):
				l+='sd.Selenium.'+base+'.'+dtitl+'.'+str(i)+':'+str()+'|ms\n'
		if (dtitl.find('Content_Delivery') != -1):
			try:
				# print('try return prs.abs_end')
				pcrT=d.execute_script("return prs.abs_end")
			except:
				pcrT=0
		elif(dtitl.find('Category_Home') != -1):
			try:
				prs=d.execute_script('return prs')
				prsT=[]
				prsT.append(prs['pcr'])
				prsT.append(prs['pcr_nav'])
				pcrT=sorted(prsT)[1]
			except:
				pcrT=0
		else:
			# print('found a different page! - '+dtitl)
			try:
				pcrT=execute_script("return prs['pcr']")
			except:
				try:
					prs=execute_script('return prs')
					pcrT=prs['pcr']
				except:
					pcrT=0
		if pcrT > navS:
			l+='sd.Selenium.'+base+'.'+dtitl+'.pcr:'+str(int(pcrT-navS))+'|ms\n'

		# print('l '+l)
	except:
		# print('scripts no workie')
		pass
	return l
