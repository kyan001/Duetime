from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404

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

def cardnoteAddcard(request):
	""" 跳转到新项目增加页面
	"""
	return render(request,'cardnote/addcard.html')

def cardnoteCreatecard(request):
	""" 增加新项目到服务器
	"""
	title = request.POST.get('title')
	kcol = request.POST.get('kcol')
	vcol = request.POST.get('vcol')
	if not title:
		raise Http404('Title cannot be empty')
	card = Notiecard(title=title, kcol=kcol, vcol=vcol)
	card.save()
	print(card.id)
	return redirect('/cardnote/list')
