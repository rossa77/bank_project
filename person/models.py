from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    national_code = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"