from django.db import models

# Create your models here.
class dailySched(models.Model):
    month = models.IntegerField()
    day = models.IntegerField()

    class Meta:
        def __unicode__(self):  #For Python 2, use __str__ on Python 3
            return self.month
