
import logging
from django.conf import settings

from crm import services

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def run():
    message = "test"
    to = "subnetix@gmail.com"
    tags = ["test"]
