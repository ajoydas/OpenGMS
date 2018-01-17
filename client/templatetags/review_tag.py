"""
This python file will create a flag that will allow
to check in the html file, if there is any review for the product. If
there is, the reviews will be showed. Otherwise,
it will show to write a review.
"""

from django.template import Library
from decimal import getcontext, Decimal
from core.models import Order
from  django.utils.timesince import timesince

register = Library()

# return time of notifications - current time
@register.assignment_tag()
def get_time(time):
    return timesince(time)