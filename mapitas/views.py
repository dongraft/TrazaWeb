import json
import locale
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Max
from django.db.models import Min

from carlitos.models import Traza


# Create your views here.
def stats(request):
    return render(request, 'mapitas/index.html', {'request':request})


def get_data(request):
    locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
    res = {}
    data = []
    vals = []
    trazas = Traza.objects.all()
    for traza in trazas:
        try:
            obj = {}
            obj['lat'] = float(traza.lat)
            obj['lng'] = float(traza.lng)
            val = int(locale.atof(traza.avg_t))
            obj['val'] = val
            data.append(obj)
            vals.append(val)
        except:
            continue
    res['data'] = data
    res['max'] = max(vals)
    res['min'] = min(vals)
    # res['min'] = int(float(trazas.aggregate(Min('avg_t'))['avg_t__min'].replace(",","")))
    return HttpResponse(json.dumps(res), content_type='application/json')
