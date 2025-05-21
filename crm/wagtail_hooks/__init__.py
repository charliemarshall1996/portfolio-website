
from wagtail.snippets.models import register_snippet

from .campaign import CampaignViewSetGroup

register_snippet(CampaignViewSetGroup)
