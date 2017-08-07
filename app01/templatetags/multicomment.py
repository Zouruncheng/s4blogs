from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def simple_comment():
    pass
