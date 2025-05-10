# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import Contact, Website  # your model
import json

from scrapers.models import SearchParameter


@csrf_exempt
def add_contacts(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            contacts = data.get("contacts", [])
            for contact in contacts:

                first_name = contact.get("first_name")
                last_name = contact.get("last_name")
                email = contact.get("email")
                url = contact.get("url")
                contact, created = Contact.objects.get_or_create(
                    first_name=first_name, last_name=last_name, email=email)
                contact.save()
                website, created = Website.objects.get_or_create(
                    url=url, contact=contact)
                website.save()

            term = data.get("term")
            location = data.get("location")

            params = SearchParameter.objects.filter(
                term=term, location=location).first()

            params.last_run_freeindex = timezone.now()
            params.save()

            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
