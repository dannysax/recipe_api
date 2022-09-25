from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User


# class UserAdmin(BaseUserAdmin):
#     list_display = ["id", "email"]

# admin.site.register(User, UserAdmin)

class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "password"]
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Permission", {"fields":("is_active", "is_superuser", "is_staff")}),
        ("Important Dates", {"fields": ("last_login",)})
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active",
            "is_staff", "is_superuser")
            }),
    )
    readonly_fields = ["last_login"]
    # list_filter = ["id"]

admin.site.register(User, UserAdmin)