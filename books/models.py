from django.db import models


class Book(models.Model):
    class Enum(models.IntegerChoices):
        HARD = 0
        SOFT = 1

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.BooleanField(choices=Enum.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.title
