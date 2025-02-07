from django.db import models

# Create your models here.


class Skill(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Qualification(models.Model):
    name = models.CharField(max_length=255)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10, blank=True, null=True)
    date_earned = models.DateField(null=True, blank=True)
    ongoing = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.name
