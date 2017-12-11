from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.db import transaction

from main.models import CardnoteCard, CardnoteItem


def cardnoteList(request):
    """Cards List"""
    context = {
        'cards_cols': [],
    }
    COLUMNS = 3  # how many columns in sm/md/lg
    cards = CardnoteCard.objects.all()
    for cl_i in range(COLUMNS):
        cl_col = [card for i, card in enumerate(cards) if i % COLUMNS == cl_i]
        context.get('cards_cols').append(cl_col)
    # render
    context['cards'] = cards
    return render(request, 'cardnote/list.html', context)


def cardnoteNewcard(request):
    """Add new card Page"""
    messages.info(request, '添加新卡片')  # only for messages testing
    return render(request, 'cardnote/newcard.html')


def cardnoteAddcard(request):
    """增加新项目到服务器"""
    title = request.POST.get('title')
    kcol = request.POST.get('kcol')
    vcol = request.POST.get('vcol')
    if not title:
        raise Http404('Title cannot be empty')
    card = CardnoteCard(title=title, kcol=kcol, vcol=vcol)
    card.save()
    print(card.id)
    # render
    messages.success(request, '新卡片《{card.title}》已添加'.format(card=card))
    return redirect('/cardnote/list')


def cardnoteDeletecard(request):
	"""删除一个卡片"""
	cardnotecardid = request.GET.get('id') or 0
	if not cardnotecardid:
		raise Http404("Id should not be empty")
	card = CardnoteCard.objects.get_or_404(id=int(cardnotecardid))
	items = card.cardnoteitems
	with transaction.atomic():
		messages.success(request, "卡片《{card.title}》已删除".format(card=card))
		card.delete()
		items.delete()
	return redirect('/cardnote/list')
