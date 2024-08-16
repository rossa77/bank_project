from faker import Faker
from .models import Person
from itertools import islice
from django.db import transaction
from django.core.exceptions import ValidationError
from bank_account.models import BankAccount
import random

def create_fake_persons(total_records, batch_size):
    fake = Faker()
    existing_codes = set(Person.objects.values_list('national_code', flat=True))

    def generate_unique():
        while True:
            code = fake.unique.numerify(text='##########')
            if code not in existing_codes:
                existing_codes.add(code)
                return code

    persons = (
        Person(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            national_code=generate_unique()
        )
        for _ in range(total_records)
    )

    while True:
        batch = list(islice(persons, batch_size))
        if not batch:
            break
        Person.objects.bulk_create(batch, batch_size)

    print(f"Total of {total_records} records created in batches of {batch_size}.")


def transfer_value(from_account_number, from_owner_firstname,from_owner_lastname, to_account_number, to_owner_firstname,to_owner_lastname, value):

    try:
        with transaction.atomic():
            from_account = BankAccount.objects.select_for_update().get(
                account_number=from_account_number,
                owner__first_name=from_owner_firstname,
                owner__last_name=from_owner_lastname
            )
            to_account = BankAccount.objects.get(
                account_number=to_account_number,
                owner__first_name=to_owner_firstname,
                owner__last_name=to_owner_lastname
            )


            if from_account.balance < value:
                raise ValidationError("not allowed.")

            from_account.balance -= value
            from_account.save()
            to_account.balance += value
            to_account.save()

            print(f"Transferred {value} from account {from_account_number} to account {to_account_number}.")

    except BankAccount.DoesNotExist:
        raise ValidationError("the accounts do not exist.")
