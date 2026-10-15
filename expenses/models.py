from django.db import models

# Create your models here.
class Expense(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="Other")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.title