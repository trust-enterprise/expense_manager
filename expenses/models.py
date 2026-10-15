from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="Other")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title