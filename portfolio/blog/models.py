
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Create your models here.
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail import blocks
from wagtail.search import index
from wagtailcodeblock.blocks import CodeBlock


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')

        paginator = Paginator(blogpages, 10)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            blogpages = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            blogpages = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            blogpages = paginator.page(paginator.num_pages)

        context['blogpages'] = blogpages
        return context


# keep the definition of BlogIndexPage model, and add the BlogPage model:

class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock(blank=True, features=[
            'h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'image', 'code'])),
        ('code', CodeBlock(label=('Code')))])
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
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
            "tags"),], heading="Blog information"), "github", "website", "data_source", "intro", FieldPanel('body'), "gallery_images",
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]
