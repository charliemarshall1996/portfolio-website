from django import template

register = template.Library()


@register.simple_tag
def url_replace(request, key, value):
    query_params = request.GET.copy()
    query_params[key] = value
    return query_params.urlencode()
