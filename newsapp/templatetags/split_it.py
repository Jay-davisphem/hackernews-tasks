import re
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def strip_it(value, arg):
    m = re.search("https?://(?:www.)?([A-Za-z_0-9.-]+).*", value)
    if m:
        return m.group(1)
