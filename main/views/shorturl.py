from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _
import jieba.analyse

from main.models import ShortUrl


def shorturlIndex(request):
    """/su"""
    return redirect("/shorturl/list")


def shorturlJump(request, id):
    """su/<int:id>"""
    shorturl = ShortUrl.objects.get_or_404(id=id)
    shorturl.add_pv()
    return redirect(shorturl.url)


@login_required
def shorturlAdd(request):
    """shorturl/add"""
    name = request.POST.get('name') or ""
    url = request.POST.get('url') or None
    user = request.user
    if request.POST:
        if not url:
            messages.error(request, _("Argument URL cannot be empty"))
        else:
            with transaction.atomic():
                shorturl = ShortUrl(name=name, url=url, userid=user.id)
                shorturl.save()
                return redirect("/shorturl/detail?id={}".format(shorturl.id))
    return render(request, "shorturl/add.html")


@login_required
def shorturlDetail(request):
    """shorturl/detail"""
    shorturlid = request.GET.get('id')
    user = request.user
    if not shorturlid:
        raise Http404(_("ShortURL ID cannot be empty"))
    shorturl = ShortUrl.objects.get_or_404(id=int(shorturlid))
    if shorturl.userid != user.id:
        raise Http404(_("You are not the owner of this shorturl"))
    context = {
        'shorturl': shorturl,
    }
    return render(request, 'shorturl/detail.html', context)


@login_required
def shorturlList(request):
    """shorturl/list"""
    user = request.user
    shorturls = ShortUrl.objects.filter(userid=user.id).order_by('-created')
    names = "".join([shorturl.name for shorturl in shorturls if shorturl.name])
    top_tags = jieba.analyse.extract_tags(names, topK=5, withWeight=False)
    CATEGORIES = ['info', 'success', 'warning', 'danger']
    for shorturl in shorturls:
        if shorturl.name:
            for tag, cate in zip(top_tags, CATEGORIES):
                if tag in shorturl.name:
                    shorturl.category = cate
                    break
        else:
            shorturl.category = "primary"
    context = {
        "shorturls": shorturls,
        "tagcate": zip(top_tags, CATEGORIES),
    }
    return render(request, 'shorturl/list.html', context)


@login_required
def shorturlDelete(request):
    """shorturl/delete"""
    shorturlid = request.GET.get('id')
    user = request.user
    if not shorturlid:
        raise Http404(_("ShortURL ID cannot be empty"))
    shorturl = ShortUrl.objects.get_or_404(id=int(shorturlid))
    if shorturl.userid != user.id:
        raise Http404(_("You are not the owner of this shorturl"))
    with transaction.atomic():
        shorturl.delete()
        messages.success(request, _("Shorturl removed!"))
        return redirect("/shorturl/list")
    raise Http404(_("Delete failed"))


@login_required
def shorturlUpdate(request):
    """shorturl/update"""
    # get inputs
    shorturlid = request.POST.get('id')
    name = request.POST.get('name') or ""
    url = request.POST.get('url') or None
    user = request.user
    if not shorturlid:
        raise Http404(_("ShortURL ID cannot be empty"))
    shorturl = ShortUrl.objects.get_or_404(id=int(shorturlid))
    if shorturl.userid != user.id:
        raise Http404(_("You are not the owner of this shorturl"))
    if not url:
        raise Http404(_("Argument URL cannot be empty"))
    with transaction.atomic():
        shorturl.name = name
        shorturl.url = url
        shorturl.save()
        messages.success(request, _("Shorturl Updated!"))
        return redirect("/shorturl/detail?id={}".format(shorturl.id))
    raise Http404(_("Update failed"))
