from django.db import models

class Traza(models.Model):
    host = models.TextField()
    ip = models.TextField()
    lat = models.TextField()
    lng = models.TextField()
    accu = models.TextField(null=True)
    p_transmitted = models.TextField(null=True)
    p_received = models.TextField(null=True)
    time = models.TextField(null=True)
    min_t = models.TextField(null=True)
    avg_t = models.TextField(null=True)
    max_t = models.TextField(null=True)
    stdev = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.created_at)
