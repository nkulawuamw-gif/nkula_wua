from django import template
from django.template.defaultfilters import stringfilter
from decimal import Decimal

register = template.Library()

@register.filter(name='currency_symbol')
def currency_symbol(user):
    try:
        if user.userprofile:
            return user.userprofile.get_currency_symbol()
    except:
        pass
    return "K"

@register.filter(name='get_logo')
def get_logo(user):
    try:
        if user.userprofile and user.userprofile.logo:
            return user.userprofile.logo.url
    except:
        pass
    return None

@register.filter
def abs(value):
    """Return the absolute value of a number."""
    try:
        return abs(value)
    except:
        return value

@register.filter
def percentage(value, total):
    """Calculate percentage of value against total"""
    try:
        if total and float(total) > 0:
            return "{:.1f}".format((float(value) / float(total)) * 100)
        return "0.0"
    except:
        return "0.0"

@register.filter
def sum_items(category_list):
    """Sum total items from category list"""
    try:
        return sum(len(cat['items']) for cat in category_list)
    except:
        return 0

@register.filter
def sum_clients(scheme_list):
    """Sum total clients from scheme list"""
    try:
        return sum(scheme['clients'] for scheme in scheme_list)
    except:
        return 0

@register.filter
def subtract(value, arg):
    """Subtract arg from value"""
    try:
        return float(value) - float(arg)
    except:
        return 0

@register.filter
def over_limit(outstanding, credit_limit):
    """Calculate amount over credit limit"""
    try:
        return float(outstanding) - float(credit_limit)
    except:
        return 0


@register.filter(name='mul')
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except:
        return 0

@register.filter(name='split')
def split(value, arg):
    """Split a string by the given delimiter"""
    try:
        if not value:
            return []
        return value.split(arg)
    except:
        return [value]

@register.filter(name='scheme_list')
def scheme_list(text):
    """Parse scheme list from database format"""
    if not text:
        return []
    result = []
    for line in text.replace('\\n', '\n').split('\n'):
        line = line.strip()
        if line and '|' in line:
            parts = line.split('|', 1)
            result.append({'name': parts[0].strip(), 'desc': parts[1].strip() if len(parts) > 1 else ''})
    return result

@register.filter(name='village_list')
def village_list(text):
    """Parse village list from database format"""
    if not text:
        return []
    result = []
    for line in text.replace('\\n', '\n').split('\n'):
        line = line.strip()
        if line and '|' in line:
            parts = line.split('|', 1)
            villages = [v.strip() for v in parts[1].split(',') if v.strip()] if len(parts) > 1 else []
            result.append({'name': parts[0].strip(), 'villages': villages})
    return result
