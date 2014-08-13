import math

from carlitos.models import Traza

trazas = Traza.objects.all()

def mean(s):
    if len(s):
        return sum(s) * 1.0 / len(s)
    else:
        return 0

tl = {'lat': -33.2926552, 'lng': -70.8520953}
br = {'lat': -33.5253681, 'lng': -70.4620807}

stgo = []

for traza in trazas:
    try:
        lat = float(traza.lat.replace(',', '.'))
        lng = float(traza.lng.replace(',', '.'))

        if lat < tl['lat'] and lat > br['lat'] and lng > tl['lng'] and lng < br['lng']:
            stgo.append(traza)
    except:
        continue

dlat = abs(tl['lat']-br['lat'])/100
dlng = abs(tl['lng']-br['lng'])/100

lat_steps = [tl['lat']-i*dlat for i in range(0,100)]
lng_steps = [tl['lng']+i*dlat for i in range(0,100)]

trazas_grid = [[[] for x in xrange(100)] for x in xrange(100)]



for traza in stgo:
    x = int(math.floor(abs(float(traza.lat.replace(',', '.'))-tl['lat'])/dlat))
    y = int(math.floor(abs(float(traza.lng.replace(',', '.'))-tl['lng'])/dlng))

    trazas_grid[x][y].append(traza)


# data = [[{} for x in xrange(100)] for x in xrange(100)]
data = []
for x in range(0,100):
    for y in range(0,100):
        traza_mean = mean([float(traza.avg_t.replace(',', '.')) for traza in trazas_grid[x][y]])
        data.append({
            'lat': lat_steps[x],
            'lng': lng_steps[y],
            'val': traza_mean,
        })






