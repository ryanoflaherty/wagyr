from django.db import models

# Create your models here.
class dailySched(models.Model):
    id = models.AutoField(primary_key=True)
    month = models.CharField(max_length=2)
    day = models.CharField(max_length=2)

    class Meta:
        def __unicode__(self):  #For Python 2, use __str__ on Python 3
            return self.month
