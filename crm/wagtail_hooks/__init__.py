
from wagtail.snippets.models import register_snippet

from .campaigns import CampaignViewSetGroup
from .dimensions import DimensionsViewSetGroup

register_snippet(CampaignViewSetGroup)
register_snippet(DimensionsViewSetGroup)
