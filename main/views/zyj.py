from django.shortcuts import render

from main.models import Notiecard, Notieitem


def zyjNotie(request):
	""" 以卡片形式记录日常
	"""
	# username = request.GET['zyj']
	# feeType = request.GET['Water']
	cards = Notiecard.objects.all()
	# render
	context = {
		'cards': cards
	}
	return render(request,'zyj/notie.html',context)
