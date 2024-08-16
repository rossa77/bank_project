from faker import Faker
from person.models import Person
from itertools import islice
from .models import BankAccount
import random
from decimal import Decimal

def create_fake_bankaccounts():
    fake = Faker()
    persons = list(Person.objects.all())
    total_records = 2000
    batch_size = 100
    bank_accounts = (
        BankAccount(
            owner=random.choice(persons),
            balance=round(random.uniform(100.00, 100000.00), 2),
            account_number=fake.unique.numerify(text='################')
        )
        for _ in range(2000)
    )
    while True:
        batch = list(islice(bank_accounts,batch_size))
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

