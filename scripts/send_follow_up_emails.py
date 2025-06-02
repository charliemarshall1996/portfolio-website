
import logging
from django.conf import settings

from crm import services

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    # get interested contacts for active campaigns
    # check they do not have a follow-up email
    # check if they have an initial outreach email for > 3 days ago
    # get email object if it isn't bounced or opted-out
    # send follow-up email
    pass
