import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from django.contrib import messages
from django.db import transaction

from main.models import CardnoteCard, CardnoteItem


@login_required
def cardnoteList(request):
    """Cards List"""
    context = {
        'cards_cols': [],
    }
    COLUMNS = 3  # how many columns in sm/md/lg
    user = request.user
    cards = CardnoteCard.objects.filter(userid=user.id)
    for cl_i in range(COLUMNS):
        cl_col = [card for i, card in enumerate(cards) if i % COLUMNS == cl_i]
        context.get('cards_cols').append(cl_col)
    # render
    context['cards'] = cards
    return render(request, 'cardnote/list.html', context)


@login_required
def cardnoteNewcard(request):
    """Add new card Page"""
    messages.info(request, 'Adding new card')  # only for messages testing
    return render(request, 'cardnote/newcard.html')


@login_required
def cardnoteAddcard(request):
    """增加新项目到服务器"""
    title = request.POST.get('title')
    kcol = request.POST.get('kcol')
    vcol = request.POST.get('vcol')
    if not title:
        raise Http404('Title cannot be empty')
    user = request.user
    card = CardnoteCard(title=title, kcol=kcol, vcol=vcol)
    card.userid = user.id
    card.save()
    # render
    messages.success(request, 'New card 《{card.title}》 added'.format(card=card))
    return redirect('/cardnote/list')


@login_required
def cardnoteDeletecard(request):
    """删除一个卡片"""
    cardnotecardid = request.GET.get('id') or 0
    if not cardnotecardid:
        raise Http404("Id should not be empty")
    user = request.user
    card = CardnoteCard.objects.get_or_404(id=int(cardnotecardid))
    if card.userid != user.id:
        raise Http404("You are not the owner of this card. Delete failed")
    items = card.cardnoteitems
    with transaction.atomic():
        messages.success(request, "Card 《{card.title}》 removed".format(card=card))
        card.delete()
        items.delete()
    return redirect('/cardnote/list')


@login_required
def cardnoteUpdate(request):
    """Update Card and Items"""
    # get inputs
    cardnotecardid = request.POST.get('id') or 0
    title = request.POST.get('title')
    kcol = request.POST.get('kcol')
    vcol = request.POST.get('vcol')
    category = request.POST.get('category') or 'default'
    new_items_in_json = request.POST.get('newitems')
    # inputs validation
    if not cardnotecardid:
        raise Http404("Id should not be empty")
    if not title:
        raise Http404('Title cannot be empty')
    # get card and items
    user = request.user
    card = CardnoteCard.objects.get_or_404(id=int(cardnotecardid))
    if card.userid != user.id:
        raise Http404("You are not the owner of this card. Update failed")
    new_items = json.loads(new_items_in_json) if new_items_in_json else []
    # update and save and delete
    with transaction.atomic():
        # card part
        card.title = title
        card.kcol = kcol
        card.vcol = vcol
        card.category = category
        card.save()
        # items part
        card.cardnoteitems.delete()
        for new_item in new_items:
            if new_item.get("kword") or new_item.get("val"):
                tmp_itm = CardnoteItem(cardnotecardid=card.id)
                tmp_itm.kword = new_item.get("kword")
                tmp_itm.val = new_item.get("val")
                tmp_itm.save()
    # render
    messages.success(request, 'Card 《{card.title}》 updated'.format(card=card))
    return redirect('/cardnote/detail?id={}'.format(card.id))


@login_required
def cardnoteDetail(request):
    """卡片详情页"""
    cardnotecardid = request.GET.get('id') or 0
    if not cardnotecardid:
        raise Http404("Id should not be empty")
    user = request.user
    card = CardnoteCard.objects.get_or_404(id=int(cardnotecardid))
    if card.userid != user.id:
        raise Http404("You are not the owner of this card.")
    context = {
        'card': card
    }
    return render(request, 'cardnote/detail.html', context)
