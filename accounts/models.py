from django.db import models
from django.core.validators import MinValueValidator

class Hive(models.Model):
    name = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    sound = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    
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