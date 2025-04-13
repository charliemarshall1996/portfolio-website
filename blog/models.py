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
        'blog.BlogPostPage', on_delete=models.CASCADE, related_name='tagged_items')


class BlogIndexPage(Page):
    # Parent page type (this will be the container for blog posts)
    subpage_types = ['blog.BlogPostPage']


class BlogPostPage(Page):
    date_published = models.DateTimeField()
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='media/blog/images/')
    summary = models.CharField(max_length=250)
    body = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('captioned_image', blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('caption', blocks.CharBlock(required=False)),
        ], icon='image')),
        ('image', ImageChooserBlock(icon='image')),
        ('code', blocks.StructBlock([
            ('language', blocks.ChoiceBlock(choices=[
                ('python', 'Python'),
                ('javascript', 'JavaScript'),
                ('html', 'HTML'),
                ('css', 'CSS'),
                ('bash', 'Bash'),
            ])),
            ('code', blocks.TextBlock()),
        ], icon='code')),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date_published'),
        FieldPanel('thumbnail'),
        FieldPanel('summary'),
        FieldPanel('body'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
