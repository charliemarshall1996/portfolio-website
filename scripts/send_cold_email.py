from django.utils import timezone
from django.core.mail import send_mail
from django.db.models import Exists, OuterRef
from datetime import timedelta
from crm import models


def make_email_body(first_name):
    return f"""
            Hi {first_name},

            Ever wonder how many people visit your website... and leave without booking?

            As someone who works closely with health and beauty professionals across Aldershot, I often hear:

            - "I don't even know if my website's doing anything."
            - "It's outdated, but I've been too busy to deal with it."
            - "I hate fiddling with tech - I just want it to work."

            I totally get it - your priority is giving your clients a great experience, not worrying about plugin updates, slow load times, or whether Google is even showing your site.

            That's where I come in. I offer done-for-you website management tailored for service businesses like yours. No faff, no stress. Just a fast, secure, on-brand site that quietly brings in more clients while you focus on what you're brilliant at.

            Would it be worth a quick 15-minute chat to see if this would help your business?
            No pressure - if it's not a fit, I'll say so.

            Cheers,
            Charlie Marshall,
            Local Web Manager | Aldershot
            07464 706 184 | https://www.charlie-marshall.dev

            P.S. I'm local, I speak human, and I keep tech stuff simple. If that sounds like your kind of help - just hit reply.
            """


def run():

    six_months_ago = timezone.now() - timedelta(days=180)

    recent_comms = models.Communication.objects.filter(
        contact=OuterRef('pk'),
        made_on__gte=six_months_ago
    )

    contacts_no_recent_comms = list(models.Contact.objects.annotate(
        has_recent_comm=Exists(recent_comms)
    ).filter(has_recent_comm=False, email_opt_out=False).order_by('created_at')[:10])

    for contact in contacts_no_recent_comms:
        body = make_email_body(contact.first_name)
        subject = "Is your website helping you stand out in the local beauty scene?"
        send_mail(subject=subject, message=body,
                  recipient_list=[contact.email],
                  from_email="charlie@charlie-marshall.dev")
        models.Communication.objects.create(contact=contact, subject=subject, body=body,
                                            made_on=timezone.now(), medium="email",
                                            direction="out", communication_type="cold")
