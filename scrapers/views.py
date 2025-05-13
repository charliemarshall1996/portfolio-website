from django.http import JsonResponse
from .models import SearchParameter


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SearchParameterSerializer
from django.utils.timezone import now


class SearchParameterView(APIView):
    def post(self, request, pk):
        try:
            search_param = SearchParameter.objects.get(pk=pk)
        except SearchParameter.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        update_target = request.data.get("directory")

        if update_target == "thomson":
            search_param.last_run_thomson = now()
        elif update_target == "freeindex":
            search_param.last_run_freeindex = now()
        else:
            return Response({"detail": "Invalid directory value."},
                            status=status.HTTP_400_BAD_REQUEST)

        search_param.save()
        return Response(SearchParameterSerializer(search_param).data)

    def get(self, request, directory):

        if directory == "thomson":
            order = "last_run_thomson"
        else:
            return Response({"detail": "Invalid directory"},
                            status=status.HTTP_400_BAD_REQUEST)
        search_param = SearchParameter.objects.all().order_by(order).first()

        if not search_param:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(data=SearchParameterSerializer(search_param).data)
