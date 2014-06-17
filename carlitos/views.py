from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed

from carlitos.models import Traza

# Create your views here.
@csrf_exempt
def receive(request):
    if request.method == 'POST':
        line = request.POST.get('data',None)
        if line:
            line = line.split(" ")
            kwargs = {
                'mobile_id': line[0]
                'timestamp': line[1]
                'host': line[2]
                'p_transmitted': line[3]
                'p_received': line[4]
                'p_lost': line[5]
                'time': line[6]
                'min_t': line[7]
                'avg_t': line[8]
                'max_t': line[9]
                'stdev': line[10]
                'lat': line[11]
                'lng': line[12]
                'accu': line[13]
            }
            try:
                traza = Traza.objects.create(**kwargs)
            except:
                return HttpResponse('{"status": "fail"}', content_type="application/json")
        return HttpResponse('{"status": "success"}', content_type="application/json")
    else:
        return HttpResponseNotAllowed(['POST'])
