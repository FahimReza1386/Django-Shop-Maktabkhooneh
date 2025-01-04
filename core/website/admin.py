from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from website.models import Contact
# Register your models here.

class CustomContact(admin.ModelAdmin):
    model=Contact
    list_display=("email", "subject", "is_checked",)
    list_filter=("is_checked",)
    searching_fields=("first_name", "last_name", "subject", "phone_number", "description",)
    ordering=("is_checked",)



admin.site.register(Contact, CustomContact)