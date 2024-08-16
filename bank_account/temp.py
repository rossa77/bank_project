from faker import Faker
from person.models import Person
from itertools import islice
from .models import BankAccount
from decimal import Decimal
from django.db.models import Q
import time
import random
def create_fake_bankaccounts(total_records, batch_size):
    fake = Faker()
    persons = list(Person.objects.all())

    existing_account = set(BankAccount.objects.values_list('account_number', flat=True))

    def generate_unique():
        while True:
            account_number = fake.unique.numerify(text='################')
            if account_number not in existing_account:
                existing_account.add(account_number)
                return account_number

    bank_accounts = (
        BankAccount(
            owner=random.choice(persons),
            balance=round(random.uniform(100.00, 10000000.00), 2),
            account_number=generate_unique()
        )
        for _ in range(total_records)
    )

    while True:
        batch = list(islice(bank_accounts, batch_size))
        if not batch:
            break
        BankAccount.objects.bulk_create(batch, batch_size)

    print(f"Total of {total_records} records created in batches of {batch_size}.")


def get_higher_national_code():

    all_accounts = BankAccount.objects.select_related('owner').all()
    accounts = []
    for account in all_accounts:
        try:
            national_code= Decimal(account.owner.national_code)
            balance = account.balance
            if national_code > balance:
                accounts.append(account)
        except (ValueError, InvalidOperation):
            continue

    return accounts


def try_without_index():
    start_time = time.time()
    accounts = BankAccount.objects.filter(Q(balance__gt=2000000) | Q(balance__lt=1000000))
    end_time = time.time()
    print(f"Query without index took: {end_time - start_time} seconds")
def try_with_index():
    start_time = time.time()
    accounts = BankAccount.objects.filter(Q(balance__gt=2000000) | Q(balance__lt=1000000))
    end_time = time.time()
    print(f"Query with index took: {end_time - start_time} seconds")