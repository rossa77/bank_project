from django.db import models
from person.models import Person

class BankAccount(models.Model):
    owner = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='accounts')
    balance = models.DecimalField(max_digits=10,decimal_places=2)
    account_number = models.CharField(max_length=16,unique=True,primary_key=True)
    #Remove comment to create index
    # class Meta:
    #     indexes = [
    #         models.Index(fields=['balance']),  # تعریف ایندکس بر روی فیلد balance
    #     ]

    def __str__(self):
        return f"Account number : {self.account_number}  And Account owner :{self.owner}"