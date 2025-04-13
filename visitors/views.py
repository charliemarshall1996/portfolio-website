from rest_framework import (views,
                            permissions,
                            response,
                            viewsets)
from django.db.models import Count
from . import models, serializers


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = models.Visitor.objects.all()
    serializer_class = serializers.VisitorSerializer
    permission_classes = [permissions.IsAdminUser]


"""class VisitorStatsAPI(views.APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        visitors_per_day = models.Visitor.objects.annotate(
            day=TruncDay('first_visited')
        ).values('day').annotate(count=Count('id')).order_by('day')

        browsers = models.Visitor.objects.values('browser').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        return response.Response({
            'visitors_per_day': list(visitors_per_day),
            'browsers': list(browsers),
        })
"""
