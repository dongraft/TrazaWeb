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
                'mobile_id': line[0],
                'timestamp': line[1],
                'host': line[2],
                'host_ip': line[3],
                'p_transmitted': line[4],
                'p_received': line[5],
                'p_lost': line[6],
                'time': line[7],
                'min_t': line[8],
                'avg_t': line[9],
                'max_t': line[10],
                'stdev': line[11],
                'lat': line[12],
                'lng': line[13],
                'accu': line[14],
                'networktype': line[15],
                'compania': line[16],
            }
            try:
                traza = Traza.objects.create(**kwargs)
            except:
                return HttpResponse('{"status": "fail"}', content_type="application/json")
        return HttpResponse('{"status": "success"}', content_type="application/json")
    else:
        return HttpResponseNotAllowed(['POST'])
