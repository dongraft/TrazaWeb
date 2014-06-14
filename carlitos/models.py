from django.db import models

class Traza(models.Model):
    host = models.CharField(max_length=64)
    ip = models.CharField(max_length=64)
    lat = models.CharField(max_length=64)
    lng = models.CharField(max_length=64)
    accu = models.CharField(max_length=64)
    p_transmitted = models.CharField(max_length=64)
    p_received = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    min_t = models.CharField(max_length=64)
    avg_t = models.CharField(max_length=64)
    max_t = models.CharField(max_length=64)
    stdev = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.created_at)
