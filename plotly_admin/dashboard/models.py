from django.db import models

class SalesData(models.Model):
    product = models.CharField(max_length=100)
    region = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product} - {self.region}"