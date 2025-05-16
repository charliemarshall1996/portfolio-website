# views.py
from . import models
from django.shortcuts import render, get_object_or_404
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import ContactSerializer


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_contact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


accessibility_intro = """
Accessibility evaluates how easily people with disabilities can use your site, 
including those using screen readers or navigating by keyboard. It checks things like 
contrast ratios, semantic HTML, and ARIA roles. Poor accessibility locks out a 
significant portion of users, harms user experience, and can expose your site to legal 
risk. More importantly, inclusive design often overlaps with good UX for everyone, 
improving engagement and conversion across the board.
"""

best_practices_intro = """
This category checks for modern, secure, and maintainable coding standards—like HTTPS 
usage, safe JavaScript practices, and avoiding outdated APIs. Ignoring these often leads
to security vulnerabilities, broken functionality, or trust issues. Following best 
practices ensures your site runs smoothly across browsers and devices, fostering trust 
and keeping users engaged—critical for conversions.
"""

performance_intro = """
Performance measures how fast your site loads and becomes usable, focusing on metrics 
like First Contentful Paint and Time to Interactive. A slow site frustrates users, 
increases bounce rates, and tanks conversions—especially on mobile. Google also uses 
performance signals for search rankings, so optimizing this directly impacts both 
traffic and the user journey.
"""

seo_intro = """
SEO audits check whether your site is discoverable and indexable by search engines, 
including proper meta tags, semantic HTML, and link structure. Strong SEO ensures your 
content surfaces in search results, driving organic traffic. Weak SEO means fewer eyes 
on your site—no traffic means no conversions, no growth.
"""


def audit_view(request, token):
    print("Getting audit...")
    analysis = get_object_or_404(models.Analysis, access_token=token)
    context = dict(analysis.data)
    context["url"] = analysis.website.url
    context["contact_name"] = models.Lead.objects.get(
        pk=analysis.website.lead_id
    ).first_name
    context["date"] = analysis.updated_at

    scores = {k: v * 100 for k, v in context["scores"].items()}
    scores["best_practices"] = scores["best-practices"]
    context["scores"] = scores
    sections = context["sections"]
    for s in sections:
        if s["name"] == "Accessibility":
            s["formatted_name"] = "accessibility"
            s["intro"] = accessibility_intro
        elif s["name"] == "Best-practices":
            s["intro"] = best_practices_intro
            s["name"] = "Best Practices"
            s["formatted_name"] = "best-practices"
        elif s["name"] == "Performance":
            s["intro"] = performance_intro
            s["formatted_name"] = "performance"
        else:
            s["intro"] = seo_intro
            s["formatted_name"] = "seo"

    context["sections"] = sections
    context["dark_sections"] = ["best practices", "seo"]
    print(context)
    for s in context["sections"]:
        audits = s["audits"]
        for a in audits:
            print(a.keys())
    return render(request, "website/full_report.html", context=context)
