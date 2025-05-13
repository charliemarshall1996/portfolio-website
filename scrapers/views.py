from django.http import JsonResponse
from .models import SearchParameter


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SearchParameter
from .serializers import SearchParameterSerializer
from django.utils.timezone import now


class UpdateSearchRunView(APIView):
    def post(self, request, pk):
        try:
            search_param = SearchParameter.objects.get(pk=pk)
        except SearchParameter.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        update_target = request.data.get("update_field")

        if update_target == "thomson":
            search_param.last_run_thomson = now()
        elif update_target == "freeindex":
            search_param.last_run_freeindex = now()
        else:
            return Response({"detail": "Invalid update_field value."},
                            status=status.HTTP_400_BAD_REQUEST)

        search_param.save()
        return Response(SearchParameterSerializer(search_param).data)


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
        "pk": param.pk,
        "location": param.location.name,
        "term": param.term.term
    })
