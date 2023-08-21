from django.utils.translation import gettext_lazy as _
from django.db import models


class Passenger(models.Model):
    class SexChoices(models.TextChoices):
        male = "male", _("Male")
        female = "female", _("Female")

    PassengerId = models.PositiveBigIntegerField(unique=True)
    Survived = models.BooleanField()
    Pclass = models.SmallIntegerField()
    Name = models.CharField(max_length=200)
    Sex = models.CharField(max_length=15, choices=SexChoices.choices)
    # max_digits=5 supports a max value of 999.99
    Age = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2)
    SibSp = models.IntegerField()
    Parch = models.IntegerField()
    Ticket = models.CharField(max_length=20)
    Fare = models.DecimalField(max_digits=10, decimal_places=4)
    Cabin = models.CharField(max_length=20, blank=True, null=True)
    Embarked = models.CharField(max_length=1, blank=True, null=True)
