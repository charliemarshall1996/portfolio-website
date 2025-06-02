from .campaign import CampaignSearchParameter


def sync_campaign_search_parameters(campaign):
    search_term = campaign.vertical.search_term
    current_locations = set(
        campaign.campaignsearchlocation_set.values_list("search_location_id", flat=True)
    )

    existing_params = CampaignSearchParameter.objects.filter(campaign=campaign)
    existing_map = {p.location_id: p for p in existing_params}

    for location_id in current_locations:
        if location_id in existing_map:
            param = existing_map[location_id]
            if not param.is_active:
                param.is_active = True
                param.save(update_fields=["is_active"])
        else:
            CampaignSearchParameter.objects.create(
                campaign=campaign,
                search_term=search_term,
                location_id=location_id,
                is_active=True,
            )

    for location_id, param in existing_map.items():
        if param.is_active and location_id not in current_locations:
            param.is_active = False
            param.save(update_fields=["is_active"])
