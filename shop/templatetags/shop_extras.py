from django.db.models import Sum,F,FloatField
from django import template


register = template.Library()

@register.filter
def total(order):
    return order.aggregate(total=Sum(F('quantity')*F('good__price'), output_field=FloatField()))['total']