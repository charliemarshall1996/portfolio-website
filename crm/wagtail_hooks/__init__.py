
from wagtail.snippets.models import register_snippet

from .campaigns import CampaignViewSetGroup
from .dimensions import DimensionsViewSetGroup
from .entities import EntityViewSetGroup

register_snippet(CampaignViewSetGroup)
register_snippet(DimensionsViewSetGroup)
register_snippet(EntityViewSetGroup)
