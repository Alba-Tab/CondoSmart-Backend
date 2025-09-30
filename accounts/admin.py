from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("pk","username","ci","email","is_active","is_staff")
    search_fields = ("username","ci","email")
    list_filter = ("is_active","is_staff", "groups__name")
