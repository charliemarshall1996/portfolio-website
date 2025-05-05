from rest_framework import permissions, response, viewsets
from rest_framework.decorators import action
from django.db.models import Count, Sum, functions
from . import models, serializers


class VisitorViewSet(viewsets.ModelViewSet):
    queryset = models.Visitor.objects.all()
    serializer_class = serializers.VisitorSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=["get"])
    def stats(self, request):
        # Date filtering
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        queryset = self.filter_queryset(self.get_queryset())

        if start_date and end_date:
            queryset = queryset.filter(
                first_visited__date__gte=start_date, first_visited__date__lte=end_date
            )

        # Aggregate data
        device_data = queryset.values("device").annotate(total=Count("id"))
        browser_data = queryset.values("browser").annotate(total=Count("id"))
        time_series = (
            queryset.annotate(date=functions.TruncDate("first_visited"))
            .values("date")
            .annotate(visits=Count("id"), pageviews=Sum("page_views"))
            .order_by("date")
        )

        # Top pages calculation
        private_pages = ["favicon", "static", "media", "admin", "visitors", "crm"]
        all_pages = []
        for visitor in queryset:
            visited_pages = visitor.visited_pages
            for page in visited_pages:
                if (
                    page.split("/")[1] not in private_pages
                    and page.split("/")[-1] != "favicon.ico"
                ):
                    all_pages.append(page)
        from collections import Counter

        top_pages = Counter(all_pages).most_common(5)

        return response.Response(
            {
                "devices": device_data,
                "browsers": browser_data,
                "time_series": time_series,
                "top_pages": [{"page": p[0], "views": p[1]} for p in top_pages],
            }
        )
