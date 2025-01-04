from django import template

register = template.Library()

@register.filter
def bytes_to_mb(value):
    """Convertit une taille en octets en mégaoctets."""
    try:
        mb_value = value / (1024 * 1024)  
        return f"{mb_value:.2f}"  
    except (TypeError, ValueError):
        return "Invalid size"
