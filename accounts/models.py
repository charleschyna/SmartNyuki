from django.db import models

class Hive(models.Model):
    name = models.CharField(max_length=50)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    sound = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
