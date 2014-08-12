# -*- coding: utf-8 -*-
import json
import locale
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Max
from django.db.models import Min
from django.views.decorators.csrf import csrf_exempt

from carlitos.models import Traza


# Create your views here.
def stats(request):
    if request.method == 'GET':
        companies = {
            'Claro': '0\n',
            'Entel': '1\n',
            'Movistar': '2\n',
            'Nextel': '3\n',
            'Virgin Mobile': '4\n',
            'VTR': '5\n',
        }
        networktypes = {
            'EDGE': '1', '3G': '2', '3.5G': '3', '4G': '3',
        }
        times = {
            'Mañana (6am a 2pm)': '6',
            'Tarde (2pm a 10pm)': '14',
            'Noche (10pm a 6am)': '22',
        }
        data = {
            'companies': companies,
            'networktypes': networktypes,
            'times': times,
        }
        return render(request, 'mapitas/index.html', data)
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
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
                val = locale.atof(traza.avg_t)
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
    else:
        return HttpResponseNotAllowed(['GET'])


def get_graphs(request):
    pass
