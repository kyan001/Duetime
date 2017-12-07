from django.shortcuts import render

def zyjNotie(request):
	""" 以卡片形式记录日常
	"""
	# username = request.GET['zyj']
	# feeType = request.GET['Water']
	# render
	context = {
		'date': '日期',
		'price': '元',
		'attri_detail': {
				'2016-11-01': '15',
				'2016-11-03': '2',
				'2016-11-06': '6',
		},

	}
	return render(request,'zyj/notie.html',context)
