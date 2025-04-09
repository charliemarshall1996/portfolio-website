import logging

from django.core.mail import send_mail
from django.utils import timezone

from rest_framework import views, status
from rest_framework.response import Response

from core.utils import is_valid_date

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
        logger.debug("Received booking GET request...")
        logger.debug("Booking date %s", date)
        if not is_valid_date(date, "%Y-%m-%d"):
            logger.error("Invalid date")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logger.debug("Valid date")
        date = date.split('-')
        date = timezone.datetime(
            year=int(date[0]), month=int(date[1]), day=int(date[2]))
        bookings = Booking.objects.filter(date=date)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request, date):
        # Parse the date from the URL
        if not is_valid_date(date, "%Y-%m-%d"):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            first_name = serializer.data['first_name']
            date = serializer.data['date']
            start_time = serializer.data['time']
            email = serializer.data['email']
            message = get_booking_confirmation_message(
                first_name, date, start_time)
            send_mail("Meeting Confirmation Email - Charlie Marshall Web Development", message=message,
                      from_email="charlie@charlie-marshall.dev", recipient_list=[email])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
