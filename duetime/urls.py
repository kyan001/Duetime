"""duetime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including anot9jher URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import main.views.beijingmore
import main.views.index
import main.views.cardnote

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # index
    url(r'^$', main.views.index.index, name='index'),
    # beijingmore
    url(r'^beijingmore$', main.views.beijingmore.beijingmoreIndex),
    url(r'^beijingmore/food$', main.views.beijingmore.beijingmoreFood),
    url(r'^beijingmore/music$', main.views.beijingmore.beijingmoreMusic),
    url(r'^cardnote/list$', main.views.cardnote.cardnoteList),
    url(r'^cardnote/addcard$', main.views.cardnote.cardnoteAddcard),
    url(r'^cardnote/createcard$', main.views.cardnote.cardnoteCreatecard),
]
