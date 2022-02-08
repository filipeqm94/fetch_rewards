from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    points = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Transaction(models.Model):
    payer = models.ForeignKey(
        Customer, related_name="transactions", on_delete=models.CASCADE
    )
    points = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
