from django.contrib import admin
from website.models import Contact, NewsletterSubscriber
# Register your models here.

class CustomContact(admin.ModelAdmin):
    model=Contact
    list_display=("email", "subject", "is_checked",)
    list_filter=("is_checked",)
    searching_fields=("first_name", "last_name", "subject", "phone_number", "description",)
    ordering=("is_checked",)

class CustomNewLatter(admin.ModelAdmin):
    model= NewsletterSubscriber
    list_display=("email",)
    ordering=("email",),

admin.site.register(Contact, CustomContact)
admin.site.register(NewsletterSubscriber, CustomNewLatter)