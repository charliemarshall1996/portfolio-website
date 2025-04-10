from django.contrib import admin
from .models import Contact, Company, Interaction

# Register your models here.

admin.site.register(Contact)
admin.site.register(Company)
admin.site.register(Interaction)
