from django.shortcuts import render


def beijingmoreIndex(request):
    return render(request, 'beijingmore/index.html')


def beijingmoreFood(request):
    return render(request, 'beijingmore/food.html')


def beijingmoreMusic(request):
    return render(request, 'beijingmore/music.html')
