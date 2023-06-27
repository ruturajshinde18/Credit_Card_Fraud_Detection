from operator import imod
from django.db import models
from account.models import Profile

# Create your models here.
class Prediction(models.Model):
    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    trans_date_trans_time = models.DateTimeField(null=True, blank=True)
    cc_num = models.CharField(max_length=100, null = True, blank = True)
    merchant = models.CharField(max_length=100, null = True, blank = True)
    category = models.CharField(max_length=100, null = True, blank = True)
    amt = models.FloatField(null=True, blank=True)
    first = models.CharField(max_length=100, null = True, blank = True)
    last = models.CharField(max_length=100, null = True, blank = True)
    gender = models.CharField(max_length=100, null = True, blank = True)
    street = models.CharField(max_length=100, null = True, blank = True)
    city = models.CharField(max_length=100, null = True, blank = True)
    zipcode = models.CharField(max_length=100, null = True, blank = True)
    lat = models.CharField(max_length=100, null = True, blank = True)
    long = models.CharField(max_length=100, null = True, blank = True)
    trans_num = models.CharField(max_length=100, null = True, blank = True)
    unix_time = models.CharField(max_length=100, null = True, blank = True)
    merch_lat = models.CharField(max_length=100, null = True, blank = True)
    merch_long = models.CharField(max_length=100, null = True, blank = True)
    is_fraud = models.IntegerField(null = True, blank = True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.name

    class Meta:
        db_table = 'predictions'