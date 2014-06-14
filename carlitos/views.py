from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed

from carlitos.models import Traza

# Create your views here.
@csrf_exempt
def receive(request):
    if request.method == 'POST':
        kwargs = {
            'host': request.POST.get('host',None),
            'ip': request.POST.get('ip',None),
            'lat': request.POST.get('lat',None),
            'lng': request.POST.get('lng',None),
            'accu': request.POST.get('accu',None),
            'p_transmitted': request.POST.get('p_transmitted',None),
            'p_received': request.POST.get('p_received',None),
            'time': request.POST.get('time',None),
            'min_t': request.POST.get('min_t',None),
            'avg_t': request.POST.get('avg_t',None),
            'max_t': request.POST.get('max_t',None),
            'stdev': request.POST.get('stdev',None),
        }
        try:
            traza = Traza.objects.create(**kwargs)
        except:
            return HttpResponse('{"status": "fail"}', content_type="application/json")
        return HttpResponse('{"status": "success"}', content_type="application/json")
    else:
        return HttpResponseNotAllowed(['POST'])
