from django import template

register = template.Library()

@register.simple_tag
def get_rate(crit, rates):
    return rates.get(crit=crit).rate