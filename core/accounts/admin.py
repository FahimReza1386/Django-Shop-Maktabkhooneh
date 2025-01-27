from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile
from django.contrib.sessions.models import Session

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = User 
    list_display=('email' , 'is_staff' , 'is_active' , 'is_superuser' , 'is_verified', "type")
    list_filter=('is_staff','is_superuser' , 'is_active' , 'is_verified',"type")
    searching_fields = ('email',)
    ordering=('email',)
    fieldsets=(
        ('Authentications', {
            "fields" : (
                "email" , 'password'
            )
        }),
        ('Permission', {
            "fields" : (
                "is_staff" , 'is_superuser' , 'is_active' , 'is_verified'
            )
        }),
        ('group Permission', {
            "fields" : (
                'groups' , 'user_permissions', "type"
            )
        }),
        ('important date', {
            "fields" : (
                'last_login' ,
            )
        }),
    )

    add_fieldsets= (
        (None , {
            'classes' : ('wide',),
            'fields' : ('email' , 'password1' , 'password2' ,'is_staff' , 'is_active' , 'is_superuser', "type")
        }),
    )



class CustomProfileModel(admin.ModelAdmin):
    model=Profile
    list_display=("id", "user", "first_name", "last_name", "phone_number","gender")
    searching_fields = ('user', "first_name", "last_name", "phone_number")

admin.site.register(Profile, CustomProfileModel)
admin.site.register(User , CustomUserAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)