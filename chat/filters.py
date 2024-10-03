from django import template

register = template.Library()

@register.filter
def naturaltime(value):
    now = timezone.now()
    diff = now - value
    seconds = diff.total_seconds()
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days:
        return f"{int(days)} дней назад"
    elif hours:
        return f"{int(hours)} часа назад"
    elif minutes:
        return f"{int(minutes)} минуты назад"
    else:
        return f"{int(seconds)} секунд назад"
