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

partition = 150

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

        ################

        def mean(s):
            if len(s):
                return sum(s) * 1.0 / len(s)
            else:
                return 0

        # tl = {'lat': -33.2926552, 'lng': -70.8520953}
        # br = {'lat': -33.5253681, 'lng': -70.4620807}

        # cuadrado
        tl = {'lat': -33.3068716, 'lng': -70.8712029}
        br = {'lat': -33.693542, 'lng': -70.2245325}

        stgo = []

        for traza in trazas:
            try:
                lat = float(traza.lat.replace(',', '.'))
                lng = float(traza.lng.replace(',', '.'))

                if lat < tl['lat'] and lat > br['lat'] and lng > tl['lng'] and lng < br['lng']:
                    stgo.append(traza)
            except:
                continue

        dlat = abs(tl['lat']-br['lat'])/partition
        dlng = abs(tl['lng']-br['lng'])/partition

        lat_steps = [tl['lat']-i*dlat for i in range(0,partition)]
        lng_steps = [tl['lng']+i*dlng for i in range(0,partition)]

        trazas_grid = [[[] for x in xrange(partition)] for x in xrange(partition)]



        for traza in stgo:
            x = int(math.floor(abs(float(traza.lat.replace(',', '.'))-tl['lat'])/dlat))
            y = int(math.floor(abs(float(traza.lng.replace(',', '.'))-tl['lng'])/dlng))

            trazas_grid[x][y].append(traza)


        data = []
        avg_ts = []
        for x in range(0,partition):
            for y in range(0,partition):
                traza_mean = mean([float(traza.avg_t.replace(',', '.')) for traza in trazas_grid[x][y]])
                avg_ts.append(traza_mean)
                data.append({
                    'lat': lat_steps[x],
                    'lng': lng_steps[y],
                    'val': traza_mean,
                })

        ################

        # for traza in stgo:
        #     try:
        #         obj = {}
        #         obj['lat'] = float(traza.lat)
        #         obj['lng'] = float(traza.lng)
        #         val = locale.atof(traza.avg_t.replace(',','.'))
        #         #val = float(traza.avg_t)
        #         obj['val'] = val

        #         avg_ts.append(val)
        #         stdevs.append(locale.atof(traza.stdev.replace(',','.')))

        #         data.append(obj)
        #         # vals.append(val)
        #     except:
        #         continue

        res['data'] = data
        #max y min los dejo estaticos para no tener que calcularlos con cada request
        res['max'] = 1000.137 #unos cuantos mas abajo
        res['min'] = 8.355 #min

        # xxx registros, media, stdev
        data_len = len(stgo)
        res['total'] = data_len
        if data_len:
            avg = mean(avg_ts)
            variance = map(lambda x: (x - avg)**2, avg_ts)

            res['stddev'] = round(math.sqrt(mean(variance)),3)
            res['average'] = round(avg,3)
        else:
            res['stddev'] = 0
            res['average'] = 0

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

