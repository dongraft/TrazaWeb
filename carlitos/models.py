from django.db import models

class Traza(models.Model):
    mobile_id = models.CharField(max_length=16)
    timestamp = models.CharField(max_length=64)
    host = models.CharField(max_length=64)
    host_ip = models.CharField(max_length=15)
    p_transmitted = models.CharField(max_length=64)
    p_received = models.CharField(max_length=64)
    p_lost = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    min_t = models.CharField(max_length=64)
    avg_t = models.CharField(max_length=64)
    max_t = models.CharField(max_length=64)
    stdev = models.CharField(max_length=64)
    lat = models.CharField(max_length=64)
    lng = models.CharField(max_length=64)
    accu = models.CharField(max_length=64)
    networktype = models.CharField(max_length=2)
    compania = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.created_at)

