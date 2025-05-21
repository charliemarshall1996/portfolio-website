
from faker import Faker
import pytest
from crm.models import (
    Entity,
    Contact,
    Lead,
    Company
)

faker = Faker()


@pytest.fixture
def contact_entity_data_factory():
    return {
        'name': f'{faker.first_name()} {faker.last_name()}',
        'notes': faker.paragraph(5),
        'is_company': False
    }


@pytest.fixture
def contact_data_factory(contact_entity_data_factory):
    def factory(*args, **kwargs):
        entity_data = contact_entity_data_factory(*args, **kwargs)
        name = entity_data['name']
        name_parts = name.split(" ")
        first_name = name_parts[0]
        last_name = name_parts[1]
        entity = Entity(**entity_data)
        entity.save()
