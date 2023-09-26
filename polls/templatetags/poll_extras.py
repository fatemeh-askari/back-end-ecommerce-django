from django import template
# from jalali_date import date2jalali

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return '{:,}'.format(value)
