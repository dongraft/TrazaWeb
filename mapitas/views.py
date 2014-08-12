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
        return render(request, 'mapitas/index.html', {})
    else:
        return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def get_data(request):
    if request.method == 'GET':
        locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )
        res = {}
        data = []
        vals = []
        tmp = []
        companies = None
        networktypes = None

        prefilters = request.GET.get('data', None)
        if prefilters:
            filters = json.loads(prefilters) if prefilters else None
            companies = [str(company['value'])+"\n" for company in filters['companies'] if company['checked']]
            networktypes = [str(network_type['value']) for network_type in filters['networkTypes'] if network_type['checked']]
            times = [time['value'] for time in filters['times'] if time['checked']]
        if companies and networktypes:
            trazas = Traza.objects.filter(compania__in=companies, networktype__in=networktypes)
        else:
            trazas = Traza.objects.all()

        # for traza in Traza.objects.all():
        #     val = locale.atof(traza.avg_t.replace(',',''))
        #     tmp.append(val)

        for traza in trazas:
            try:
                obj = {}
                obj['lat'] = float(traza.lat)
                obj['lng'] = float(traza.lng)
                val = locale.atof(traza.avg_t.replace(',',''))
                obj['val'] = val
                data.append(obj)
                # vals.append(val)
            except:
                continue
        res['data'] = data
        #max y min los dejo estaticos para no tener que calcularlos con cada request
        res['max'] = 296512375.0 #max
        res['max'] = 46101793.0 #unos cuantos mas abajo
        # res['max'] = max(tmp)
        res['min'] = 8.355 #min
        # res['min'] = min(tmp)
        # res['min'] = int(float(trazas.aggregate(Min('avg_t'))['avg_t__min'].replace(",","")))
        return HttpResponse(json.dumps(res), content_type='application/json')
        #return HttpResponse(json.dumps(filters), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])


def graphs(request):
    return render(request, 'mapitas/graphs.html', {})
