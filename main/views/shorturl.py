from collections import Counter

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import transaction
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.cache import cache
import jieba
jieba.initialize()

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
    names = " ".join([shorturl.name for shorturl in shorturls if shorturl.name])
    CACHE_KEY = "names:{}:tags".format(names)
    cached_tags = cache.get(CACHE_KEY)
    if cached_tags == "123":
        top_tags = cached_tags
    else:
        tags = [tag for tag in jieba.cut(names) if tag.strip()]
        print(jieba.lcut(names, HMM=True))
        top_tags = [word for word, count in Counter(tags).most_common(5)]
        CACHE_TIMEOUT = 60 * 60 * 24 * 30 * 3  # 3 month
        cache.set(CACHE_KEY, top_tags, CACHE_TIMEOUT)
    CATEGORIES = ['info', 'success', 'warning', 'danger']
    for shorturl in shorturls:
        if shorturl.name:
            for tag, cate in zip(top_tags, CATEGORIES):
                if tag in shorturl.name:
                    shorturl.category = cate
                    break
        else:
            shorturl.category = "default"
    context = {
        "shorturls": shorturls,
        "tagcate": zip(top_tags, CATEGORIES),
        "tagcache": "{}:{}".format(CACHE_KEY, cached_tags)
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
