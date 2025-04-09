
from django.utils.timezone import now, datetime, timedelta
import pytest

from booking.models import Booking


@pytest.mark.django_db
def test_create_booking():
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'company': 'Acme Corp.',
        'industry': 'Explosives',
        'email': 'john.doe@email.com',
        'description': 'booking desc.',
        'date': now().date(),
        'time': now().time()
    }

    booking = Booking(**data)
    booking.save()
    end = datetime.combine(
        data['date'], data['time']) + timedelta(minutes=15)
    assert booking.first_name == data['first_name']
    assert booking.last_name == data['last_name']
    assert booking.company == data['company']
    assert booking.industry == data['industry']
    assert booking.email == data['email']
    assert booking.description == data['description']
    assert booking.date == data['date']
    assert booking.time == data['time']
    assert booking.end == end.time()
