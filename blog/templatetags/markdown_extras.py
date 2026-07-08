import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def _nl2br(text):
    """Convert single newlines to Markdown hard breaks (two trailing spaces),
    preserving fenced code blocks and blank lines (paragraph breaks)."""
    lines = text.split("\n")
    result = []
    in_code_block = False

    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
        elif in_code_block:
            result.append(line)
        elif line.strip() == "":
            # blank line → keep as paragraph break
            result.append(line)
        else:
            # add two trailing spaces for a <br> (Markdown hard break)
            result.append(line + "  ")

    return "\n".join(result)


@register.filter(name="markdown")
def markdown_format(value):
    # Pre-process: convert single newlines to hard breaks
    value = _nl2br(value)
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
