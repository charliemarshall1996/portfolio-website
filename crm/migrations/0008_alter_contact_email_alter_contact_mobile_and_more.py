from django.db import migrations, models
from django.db.models import Count


def cleanup_emails(apps, schema_editor):
    Contact = apps.get_model('crm', 'Contact')
    duplicates = (
        Contact.objects
        .values('email')
        .annotate(count=Count('id'))
        .filter(count__gt=1, email__isnull=False)
    )
    for entry in duplicates:
        email = entry['email']
        first_contact = Contact.objects.filter(
            email=email).order_by('id').first()
        if first_contact:
            Contact.objects.filter(email=email).exclude(
                id=first_contact.id).update(email=None)


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_alter_contact_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(
                blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.RunPython(
            cleanup_emails, reverse_code=migrations.RunPython.noop),
    ]
