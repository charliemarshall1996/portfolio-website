
from wagtail.snippets.models import register_snippet
from .analyses import AnalysisViewSetGroup
from .campaigns import CampaignsSnippetViewSetGroup
from .contacts_and_entities import ContactsAndEntitiesViewsetGroup
from .dimensions import DimensionsViewSetGroup

register_snippet(AnalysisViewSetGroup)
register_snippet(CampaignsSnippetViewSetGroup)
register_snippet(ContactsAndEntitiesViewsetGroup)
register_snippet(DimensionsViewSetGroup)
