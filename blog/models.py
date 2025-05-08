from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "blog.BlogPostPage", on_delete=models.CASCADE, related_name="tagged_items"
    )


class BlogPostPage(Page):
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.PROTECT, related_name="+"
    )
    summary = models.CharField(max_length=250)
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            (
                "captioned_image",
                blocks.StructBlock(
                    [
                        ("image", ImageChooserBlock()),
                        ("caption", blocks.CharBlock(required=False)),
                    ],
                    icon="image",
                ),
            ),
            ("image", ImageChooserBlock(icon="image")),
            (
                "code",
                blocks.StructBlock(
                    [
                        (
                            "language",
                            blocks.ChoiceBlock(
                                choices=[
                                    ("python", "Python"),
                                    ("javascript", "JavaScript"),
                                    ("html", "HTML"),
                                    ("css", "CSS"),
                                    ("bash", "Bash"),
                                ]
                            ),
                        ),
                        ("code", blocks.TextBlock()),
                    ],
                    icon="code",
                ),
            ),
        ],
        use_json_field=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("thumbnail"),
        FieldPanel("summary"),
        FieldPanel("tags"),
        FieldPanel("body"),
    ]

    parent_page_types = ["blog.BlogIndexPage"]


class BlogIndexPage(Page):
    # Add any fields or methods needed for your index page

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Get live, child pages of this index page, ordered by reverse date
        blog_pages = (
            BlogPostPage.objects.live().child_of(self).order_by("-last_published_at")
        )

        # Optional: Add pagination
        from django.core.paginator import Paginator

        paginator = Paginator(blog_pages, per_page=10)
        page_number = request.GET.get("page")
        paginated_pages = paginator.get_page(page_number)

        context["blog_posts"] = paginated_pages
        return context
