from django.shortcuts import render_to_response, redirect
from main.models import *

def index(request):
    context = {'request': request}
    return render_to_response('index/index.html', context)
