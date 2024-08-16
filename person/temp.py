from faker import Faker
from .models import Person
from itertools import islice


def create_fake_persons():
    fake = Faker()

    total_records = 500
    batch_size = 100

    persons = (
        Person(
            first_name = fake.first_name(),
            last_name = fake.last_name(),
            national_code = fake.unique.numerify(text='##########')
        )
        for _ in range(500)
    )
    while True:
        batch = list(islice(persons,batch_size))
        if not batch:
            break
        Person.objects.bulk_create(batch, batch_size)
    print(f"Total of {total_records} records created in batches of {batch_size}.")
