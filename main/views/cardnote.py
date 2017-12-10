from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404

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
    return redirect('/cardnote/list')
