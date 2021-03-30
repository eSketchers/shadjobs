'''
Created on May 2, 2014

@author: Muneeb
'''

from django import template

register = template.Library()

@register.filter
def multiselect_choices(boundField):
    """
    Returns Select Multiple field's data or it's verbose version 
    for a field with choices defined.
    """
#     data = boundField.data
    field = boundField.field
    select_multiple_choices = []
    for choice in field.choices:
            select_multiple_choices.append(choice)
    
    return select_multiple_choices

