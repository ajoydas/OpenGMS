"""
This python file will create a flag that will allow
to check in the html file, if there is any review for the product. If
there is, the reviews will be showed. Otherwise,
it will show to write a review.
"""

from django.template import Library
from  django.utils.timesince import timesince

register = Library()


@register.simple_tag()
def get_item(arr, indx):
    if arr is None:
        return
    return arr[indx]