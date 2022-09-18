from django import template
from datetime import datetime, timedelta,time


register = template.Library()


@register.filter(name='from_today')
def from_today(days, format):
    return (datetime.today().date() + timedelta(days=days)).strftime(format)

