from django.db import models

# Create your models here.
# one object


class Heading(models.Model):
    SIZE_CHOICES = [
        ('H2', 'H2'),
        ('H3', 'H3'),
        ('H4', 'H4'),
        ('H5', 'H5'),
        ('H6', 'H6')
    ]

    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Heading"


class RichText(models.Model):
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Text"


class CaptionedImage(models.Model):
    image = models.ImageField(upload_to="media/blog/images/")
    text = models.TextField(null=True, blank=True)

    # StreamField option for list of objects
    as_list = True

    def __str__(self):
        return self.text[:30]

    class Meta:
        verbose_name = "Image with text"
        verbose_name_plural = "Images with text"


STREAMBLOCKS_MODELS = [
    Heading,
    RichText,
    CaptionedImage,
]
