from django import template

register = template.Library()

@register.inclusion_tag("tags/form_table_row.djhtml")
def form_table_row(form_field):
    return {'form_field': form_field }
