import sqlparse

from django import template

register = template.Library()

@register.filter
def format_sql(value):
    return sqlparse.format(str(value), reindent=True, keyword_case='upper').strip()

@register.filter
def explain(value):
    return value.explain("default", analyze=True)

