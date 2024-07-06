from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=255, blank=True, null=True)

class Threshold(models.Model):
    hive_id = models.IntegerField()
    parameter = models.CharField(max_length=100)
    value = models.FloatField()

class Hive(models.Model):
    name = models.CharField(max_length=100)
    temperature_threshold_low = models.FloatField(default=10.0)
    temperature_threshold_high = models.FloatField(default=40.0)
    humidity_threshold_low = models.FloatField(default=45.0)
    humidity_threshold_high = models.FloatField(default=70.0)
    sound_threshold_high = models.FloatField(default=70.0)

    def __str__(self):
        return self.name


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class MpesaResponseBody(AbstractBaseModel):
    body = models.JSONField()


class Transaction(AbstractBaseModel):
    phonenumber = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    receipt_no = models.CharField(max_length=100)

    def __str__(self):
        return self.receipt_no