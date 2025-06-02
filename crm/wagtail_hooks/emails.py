
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel

from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from crm.models import OptedOutEmail, BouncedEmail, Email


class EmailViewSet(SnippetViewSet):
    pass


class OptedOutEmailViewSet(SnippetViewSet):
    pass


class BouncedEmailViewSet(SnippetViewSet):
    pass


class EmailViewSetGroup(SnippetViewSetGroup):
    items = [EmailViewSet, OptedOutEmailViewSet, BouncedEmailViewSet]
    menu_icon = "mail"
    menu_name = "email"
    menu_label = "Email"
