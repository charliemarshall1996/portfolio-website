from django import forms
from . import models
import datetime


class BookingForm(forms.ModelForm):
    class Meta:
        model = models.Booking
        fields = ['first_name', 'last_name', 'company', 'industry',
                  'email', 'description', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(attrs={'id': 'id_time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize with empty time choices - they'll be populated via JavaScript
        self.fields['time'].choices = []

        # If we're editing an existing booking, include its time as an option
        if self.instance and self.instance.pk:
            self.fields['time'].choices = [
                (self.instance.time.strftime('%H:%M'),
                 self.instance.time.strftime('%H:%M'))
            ]

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            # Combine date and time to check for existing bookings
            start_datetime = datetime.datetime.combine(date, time)
            end_datetime = start_datetime + datetime.timedelta(minutes=15)

            # Check for overlapping bookings
            overlapping = models.Booking.objects.filter(
                date=date,
                time__lt=end_datetime.time(),
                end__gt=time
            ).exclude(pk=self.instance.pk if self.instance else None)

            if overlapping.exists():
                raise forms.ValidationError(
                    "This time slot is already booked. Please choose another time."
                )

        return cleaned_data

    def save(self, *args, **kwargs):
        return super().save(*args, commit=False, **kwargs)
