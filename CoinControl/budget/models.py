from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    valuta = models.CharField(max_length=50, null=False, blank=False)
    recipient = models.CharField(max_length=255, null=False, blank=False)
    notes = models.CharField(max_length=1024)

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    date_added = models.DateField(auto_now_add=True, null=False, blank=False)
    goal_date = models.DateField(null=False, blank=False)
    notes = models.CharField(max_length=1024)
    