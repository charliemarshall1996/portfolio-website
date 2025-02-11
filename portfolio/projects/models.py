
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Create your models here.
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.search import index


class ProjectIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        Projectpages = self.get_children().live().order_by('-first_published_at')
        # Paginate all posts by 2 per page
        paginator = Paginator(Projectpages, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            Projectpages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            Projectpages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            Projectpages = paginator.page(paginator.num_pages)

        context['Projectpages'] = Projectpages
        return context


# keep the definition of ProjectIndexPage model, and add the ProjectPage model:

class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProjectPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class ProjectPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=ProjectPageTag, blank=True)
    github = models.URLField(blank=True)
    website = models.URLField(blank=True)
    data_source = models.URLField(blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [MultiFieldPanel([
        "date",
        FieldPanel(
            "tags"),], heading="Project information"), "github", "website", "data_source", "intro", "body", "gallery_images",
    ]


class ProjectPageGalleryImage(Orderable):
    page = ParentalKey(ProjectPage, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]
