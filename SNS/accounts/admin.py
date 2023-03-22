from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser

##@admin.register(CustomUser)
##class CustomUserAdmin(admin.ModelAdmin):
##
##    fieldsets = (
##        (None, {"fields": ("username", "password")}),
##        ("Personal info", {"fields": ("email",)}),
##        ("Permissions", {"fields": ("is_active", "is_staff", "is_admin", "groups", "user_permissions")}),
##        ("Important dates", {"fields": ("last_login", "date_joined")}),
##    )
##
##    list_display = ("username", 'email', "last_login", 'is_staff')
##    search_fields = ("username", "email")
##    filter_horizontal = ("groups", "user_permissions")
admin.site.register(CustomUser)

