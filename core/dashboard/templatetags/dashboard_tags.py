from django import template
from datetime import datetime
import jdatetime

register = template.Library()

@register.simple_tag
def formatted_date(datetimes):
    if not datetime or not isinstance(datetimes, datetime):  
        return "تاریخ نامعتبر"  
    jalali_date = jdatetime.datetime.fromgregorian(datetime=datetimes)  
    formatted_jalali_date = jalali_date.strftime('%H:%M:%S : %Y/%m/%d')  # اضافه کردن ساعت  
    return formatted_jalali_date  