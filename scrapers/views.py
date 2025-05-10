from django.http import JsonResponse
from .models import SearchParameter


def get_oldest_searchparameter(request):
    param = (
        SearchParameter.objects
        .filter(last_run_freeindex__isnull=False)
        .order_by("last_run_freeindex")
        .select_related("location", "term")
        .first()
    )

    if not param:
        return JsonResponse({"error": "No SearchParameters found."}, status=404)

    return JsonResponse({
        "location": param.location.name,
        "term": param.term.term
    })
