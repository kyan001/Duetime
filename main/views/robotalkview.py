import json
import urllib.request
from django.shortcuts import render_to_response
from django.http import JsonResponse


def robotalkIndex(request):
    context = {'request': request}
    return render_to_response('robotalk/index.html', context)


def robotalkGetresponse(request):  # AJAX
    """Get input and take back request via AJAX"""
    userinput = request.GET.get('txt')
    if not userinput:
        return JsonResponse({'error': 'userinput is empty'})

    def getResponse(url, param):
        if param:
            param = urllib.parse.urlencode(param)
        u = urllib.request.urlopen("{u}?{p}".format(u=url, p=param))
        u_resp = u.read()
        if not u_resp:
            return None
        return u_resp.decode()
    robo1 = 'http://www.niurenqushi.com/app/simsimi/ajax.aspx'
    robo1_param = {'txt': userinput}
    robo2 = 'http://api.qingyunke.com/api.php'
    robo2_param = {
        'key': 'free',
        'appid': 0,
        'msg': userinput,
    }
    robo1_says = getResponse(robo1, robo1_param)
    robo2_resp = getResponse(robo2, robo2_param)
    result = {
        'result1': {
            'txt': robo1_says,
            'url': robo1,
            'from': 'simsimi',
        },
        'result2': {
            'txt': robo2_says,
            'url': robo2,
            'from': 'feifei',
        },
    }
    return JsonResponse(result)
