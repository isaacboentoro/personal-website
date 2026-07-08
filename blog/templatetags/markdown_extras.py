import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="markdown")
def markdown_format(value):
    html = markdown.markdown(
        value,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "toc",
        ],
        extension_configs={
            "codehilite": {
                "css_class": "highlight",
                "guess_lang": False,
                "use_pygments": True,
            },
        },
    )
    return mark_safe(html)
