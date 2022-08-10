from django import template
from django.template import Context
from django.contrib.messages import constants as message_constants


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


@register.inclusion_tag('render_submit_button.html')
def render_submit_button(label="Submit"):
    """
    Render form submit button.
    """
    return {
        "label": label
    }


@register.inclusion_tag('render_messages.html', takes_context=True)
def render_messages(context, *args, **kwargs):
    if isinstance(context, Context):
        context = context.flatten()
    context.update({"message_constants": message_constants})
    return context
