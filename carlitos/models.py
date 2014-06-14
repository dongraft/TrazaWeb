from django.db import models

class Traza(models.Model):
    host = models.TextField()
    ip = models.TextField()
    lat = models.TextField()
    lng = models.TextField()
    accu = models.TextField()
    p_transmitted = models.TextField()
    p_received = models.TextField()
    time = models.TextField()
    min_t = models.TextField()
    avg_t = models.TextField()
    max_t = models.TextField()
    stdev = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.created_at)
