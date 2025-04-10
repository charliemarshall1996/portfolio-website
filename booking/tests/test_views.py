import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase
from booking.models import Booking


@pytest.mark.django_db
class TestBookingAPI(APITestCase):

    def test_get_valid_date(self):
        today = timezone.now().date().strftime("%Y-%m-%d")
        url = reverse('booking:api', kwargs={'date': today})
        response = self.client.get(url)
        assert response.status_code == 200

    def test_get_invalid_date(self):
        today = timezone.now().date().strftime("%m-%d-%Y")
        url = reverse('booking:api', kwargs={'date': today})
        response = self.client.get(url)
        assert response.status_code == 400

    def test_post_valid_date(self):
        today = timezone.now().date().strftime("%Y-%m-%d")
        url = reverse('booking:api', kwargs={'date': today})
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'company': 'ACME Corp',
            'industry': 'chemicals',
            'time': '10:00:00',
            'date': '2025-09-05',
            'email': 'charlie.marshall1996@gmail.com',
            'description': 'test'
        }
        response = self.client.post(url, data)
        assert response.status_code == 201

        booking = Booking.objects.filter(
            first_name=data['first_name'], last_name=data['last_name']).first()
        assert booking.first_name == data['first_name']
        assert booking.last_name == data['last_name']
        assert booking.company == data['company']
        assert booking.industry == data['industry']
        assert booking.email == data['email']

    def test_post_invalid_date(self):
        today = timezone.now().date().strftime("%m-%d-%Y")
        url = reverse('booking:api', kwargs={'date': today})
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'company': 'ACME Corp',
            'industry': 'chemicals',
            'time': '10:00:00',
            'date': '2025-09-05',
            'email': 'charlie.marshall1996@gmail.com',
            'description': 'test'
        }
        response = self.client.post(url, data)
        assert response.status_code == 400

    def test_post_invalid_data(self):
        today = timezone.now().date().strftime("%m-%d-%Y")
        url = reverse('booking:api', kwargs={'date': today})
        data = {
            'first_name': 'john',
            'last_name': 'doe',
            'company': 'ACME Corp',
            'industry': 'chemicals',
            'time': '10:00:00',
            'date': '2025-09-05',
            'email': 'charlie.marshall1996',
            'description': 'test'
        }
        response = self.client.post(url, data)
        assert response.status_code == 400

    def test_post_no_data(self):
        today = timezone.now().date().strftime("%m-%d-%Y")
        url = reverse('booking:api', kwargs={'date': today})
        data = {
        }
        response = self.client.post(url, data)
        assert response.status_code == 400
