from django import template


register = template.Library()


#
# Filters
#

@register.filter(name='widget_type')
def widget_type(field):
    """
    Return the widget type
    """
    if hasattr(field, 'widget'):
        return field.widget.__class__.__name__.lower()
    elif hasattr(field, 'field'):
        return field.field.widget.__class__.__name__.lower()
    else:
        return None

#
# Inclusion tags
#

@register.inclusion_tag('render_field.html')
def render_field(field, bulk_nullable=False, label=None):
    """
    Render a single form field from template
    """
    return {
        'field': field,
        'label': label,
        'bulk_nullable': bulk_nullable,
    }


@register.inclusion_tag('render_errors.html')
def render_errors(form):
    """
    Render form errors, if they exist.
    """
    return {
        "form": form
    }
