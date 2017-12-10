from django.shortcuts import render
from django.core.context_processors import csrf
from main.models import Notiecard, Notieitem


def cardnoteList(request):
	""" 以卡片形式记录日常
	"""
	cards = Notiecard.objects.all()
	# render
	context = {
		'cards': cards
	}
	return render(request,'cardnote/list.html',context)

