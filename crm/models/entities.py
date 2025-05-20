
from uuid import uuid4
from modelcluster.models import ClusterableModel
from django.db import models


class Entity(ClusterableModel):
    # Can be "Jane Smith", or "Acme Ltd"
    uuid = models.UUIDField(default=uuid4)
    vertical = models.ForeignKey(
        'crm.Vertical', on_delete=models.SET_NULL, null=True, blank=True
    )
    campaign_search_parameter = models.ForeignKey(
        'crm.CampaignSearchParemeter', on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=255)
    is_company = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyProfile(models.Model):
    entity = models.OneToOneField('crm.Entity', on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100)
    headquarters = models.ForeignKey(
        'crm.Address', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.entity.name
