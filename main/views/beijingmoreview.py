from django.shortcuts import render_to_response, redirect
from main.models import *

def beijingmoreIndex(request):
    context = {'request': request}
    return render_to_response('beijingmore/index.html', context)

def beijingmoreFood(request):
    context = {'request': request}
    return render_to_response('beijingmore/food.html', context)

def beijingmoreMusic(request):
    context = {'request': request}
    return render_to_response('beijingmore/music.html', context)
