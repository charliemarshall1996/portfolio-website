from django.utils import timezone
from user_agents import parse  # Correct import
from .models import Visitor


class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.session_key:
            request.session.save()
        session_key = request.session.session_key

        ip = self.get_client_ip(request)

        # Get or create Visitor
        visitor, created = Visitor.objects.get_or_create(
            session_key=session_key,
            defaults={
                "ip_address": ip,
                "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                "referrer": request.META.get("HTTP_REFERER", ""),
            },
        )

        # Update visitor data
        if not created:
            visitor.page_views += 1
            visitor.visited_pages.append(request.path)
            visitor.save()
        else:
            # Parse user agent ONLY for new visitors
            self.parse_user_agent(visitor)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        return (
            x_forwarded_for.split(",")[0]
            if x_forwarded_for
            else request.META.get("REMOTE_ADDR")
        )

    def parse_user_agent(self, visitor):
        # Parse the user agent string
        ua = parse(visitor.user_agent)

        # Extract browser, OS, and device info
        visitor.browser = f"{ua.browser.family} {ua.browser.version_string}".strip()
        visitor.os = f"{ua.os.family} {ua.os.version_string}".strip()
        visitor.device = ua.device.family
        visitor.save()  # Save parsed data
