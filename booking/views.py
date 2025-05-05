from django.shortcuts import render, redirect
import datetime
from .forms import BookingForm
from django.utils import timezone
import logging

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import views, status
from rest_framework.response import Response

from core.utils import is_valid_date
from datetime import datetime

from .models import Booking
from .serializers import BookingSerializer

logger = logging.getLogger("__name__")
logger.setLevel(logging.DEBUG)


def get_booking_confirmation_message(first_name, booking_date, booking_time):
    return f"""
            Hi {first_name},
            
            This a confirmation email that you have booked a meeting with me at {booking_time} on {booking_date}.
            I will be in touch shortly to provide a meeting link to confirm this.
            I very much look forward to seeing how we can build the web app of your dreams.
            
            Many thanks,
            Charlie Marshall
            """


class BookingAPI(views.APIView):
    def get(self, request, date):
        logger.debug("Booking date %s", date)
        if not is_valid_date(date, "%Y-%m-%d"):
            logger.error("Invalid date")
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Parse the date
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        # Get all bookings for this date
        bookings = Booking.objects.filter(date=date_obj)
        booked_times = [booking.time for booking in bookings]

        return JsonResponse(booked_times)

    def post(self, request, date):
        logger.debug("post request received\nDate: %s", date)
        if not is_valid_date(date, "%Y-%m-%d"):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Changed from request.body to request.data
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            first_name = serializer.data["first_name"]
            date = serializer.data["date"]
            start_time = serializer.data["time"]
            email = serializer.data["email"]
            message = get_booking_confirmation_message(
                first_name, date, start_time)
            send_mail(
                "Meeting Confirmation Email - Charlie Marshall Web Development",
                message=message,
                from_email="charlie@charlie-marshall.dev",
                recipient_list=[email],
            )
            send_mail(
                f"New Booking from {first_name}",
                message=f"New meeting request from {first_name} at {start_time} on \
                    {date}. Email: {email}",
                from_email="charlie@charlie-marshall.dev",
                recipient_list=["charlie@charlie-marshall.dev"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_available_times(request):
    date_str = request.GET.get('date')

    if not date_str:
        return JsonResponse({'error': 'Date parameter is required'}, status=400)

    try:
        selected_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    # Business hours: 08:00 to 17:00 (last slot starts at 16:45)
    start_time = datetime.time(8, 0)
    end_time = datetime.time(17, 0)

    # Generate all possible 15-minute slots
    all_slots = []
    current_time = start_time
    while current_time < end_time:
        all_slots.append(current_time)
        # Add 15 minutes
        current_time = (datetime.datetime.combine(selected_date, current_time) +
                        datetime.timedelta(minutes=15)).time()

    # Get booked time slots for the selected date
    booked_slots = Booking.objects.filter(
        date=selected_date).values_list('time', flat=True)
    booked_slots = set(booked_slots)

    # Filter out booked slots
    available_slots = [
        (time.strftime('%H:%M'), time.strftime('%H:%M'))
        for time in all_slots if time not in booked_slots
    ]

    return JsonResponse({'times': available_slots})
