import logging
from typing import List

from django.conf import settings

import brevo_python
from brevo_python.rest import ApiException


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def send_email_via_brevo(to_email, subject, html_content, tags=[]):

    # Configure API key authorization: api-key
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    # create an instance of the API class
    api_instance = brevo_python.TransactionalEmailsApi(
        brevo_python.ApiClient(configuration))
    sender = brevo_python.SendSmtpEmailSender(
        email="charlie@charlie-marshall.dev")
    send_smtp_email = brevo_python.SendSmtpEmail(to=[{"email": to_email}],
                                                 subject=subject,
                                                 html_content=html_content,
                                                 sender=sender,
                                                 tags=tags)

    try:
        # Send a transactional email
        api_response = api_instance.send_transac_email(send_smtp_email)
        logger.info("API RESPONSE: %s", api_response)
        return api_response
    except ApiException as e:
        logger.error(
            "Exception when calling TransactionalEmailsApi->send_transac_email: %s\n",
            e)


def retrieve_initial_email(first_name, link, link_text, bullet_items,
                           greeting, intro, closing, farewell):
    if bullet_items:
        bullet_html = "<ul>"
        for bullet in bullet_items:
            bullet_html += f"<li>{bullet.content}</li>"
        bullet_html += "</ul>"
    else:
        bullet_html = ""

    return f"""
        <p>{greeting}</p>
        <p>Hi {first_name},</p>
        <p>{intro}</p>
        {bullet_html}
        <p>{closing} <a href="{link}">{link_text}</a></p>
        <p>{farewell}</p>
        <p>Charlie Marshall,<br>
        Web & Data Developer<br>
        https://www.charlie-marshall.com<br>
        07464 706 184<br>
        <a href="https://calendly.com/charlie-charlie-marshall/30min">Book a Free 
        Consultation</a></p>
    """


def retrieve_follow_up_email(first_name, link, link_text, main,
                             greeting, intro, closing, farewell):

    return f"""
        <p>{greeting}</p>
        <p>Hi {first_name},</p>
        <p>{intro}</p>
        <p>{main}</p>
        <p>{closing} <a href="{link}">{link_text}</a></p>
        <p>{farewell}</p>
        <p>Charlie Marshall,<br>
        Web & Data Developer<br>
        https://www.charlie-marshall.com<br>
        07464 706 184<br>
        <a href="https://calendly.com/charlie-charlie-marshall/30min">Book a Free 
        Consultation</a></p>
    """
