from django.shortcuts import render_to_response, redirect
from main.models import *

def beijingmore(request):
    context = {'request': request}
    return render_to_response('beijingmore/beijingmore.html', context)
