from rest_framework import views, status
from rest_framework.response import Response
from django.views.generic import CreateView
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer


class BookingAPI(views.APIView):
    def get(self, request, date):
        if date:
            date = date.split('-')
            date = timezone.datetime(
                year=int(date[0]), month=int(date[1]), day=int(date[2]))
            bookings = Booking.objects.filter(date=date)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, date):
        # Parse the date from the URL
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
