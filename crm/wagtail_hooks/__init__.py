
from wagtail.snippets.models import register_snippet

from .campaigns import CampaignViewSetGroup
from .dimensions import DimensionsViewSetGroup
from .outreach import OutreachViewSetGroup

register_snippet(CampaignViewSetGroup)
register_snippet(DimensionsViewSetGroup)
register_snippet(OutreachViewSetGroup)
