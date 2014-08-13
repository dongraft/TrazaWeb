# -*- coding: utf-8 -*-
import json
import locale
import math
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
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
        stdevs = []
        avg_ts = []
        companies = None
        networktypes = None

        prefilters = request.GET.get('data', None)
        if prefilters:
            filters = json.loads(prefilters)
            companies = [str(company['value'])+"\n" for company in filters['companies'] if company['checked']]
            networktypes = [str(network_type['value']) for network_type in filters['networkTypes'] if network_type['checked']]
            times = [time['value'] for time in filters['times'] if time['checked']]
            trazas = filter_times(Traza.objects.filter(compania__in=companies, networktype__in=networktypes), times)

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

                avg_ts.append(val)
                stdevs.append(locale.atof(traza.stdev.replace(',','')))

                data.append(obj)
                # vals.append(val)
            except:
                continue
        res['data'] = data
        #max y min los dejo estaticos para no tener que calcularlos con cada request
        res['max'] = 46101793.0 #unos cuantos mas abajo
        res['min'] = 8.355 #min

        # xxx registros, media, stdev
        res['total'] = len(data)

        def average(s): return sum(s) * 1.0 / len(s)
        avg = average(avg_ts)
        variance = map(lambda x: (x - avg)**2, avg_ts)

        res['stddev'] = round(math.sqrt(average(variance)),3)
        res['average'] = round(avg,3)

        # res['min'] = min(tmp)
        # res['min'] = int(float(trazas.aggregate(Min('avg_t'))['avg_t__min'].replace(",","")))
        return HttpResponse(json.dumps(res), content_type='application/json')
        #return HttpResponse(json.dumps(filters), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])


def graphs(request):
    return render(request, 'mapitas/graphs.html', {})

def filter_times(trazas, times):
    new_trazas = []
    for traza in trazas:
        try:
            h = int(traza.timestamp[9:11])

            # if <esta seteado el filtro> and <condicion de hora de inicio> and <condicion de hora final>
            if 1 in times and h >= 6 and h <12:
                new_trazas.append(traza)
            elif 2 in times and h >= 12 and h <20:
                new_trazas.append(traza)
            elif 3 in times and (h < 6 or h >= 20):
                new_trazas.append(traza)
        except:
            print 'ts: %s\n'%traza.timestamp
            continue
    return new_trazas

