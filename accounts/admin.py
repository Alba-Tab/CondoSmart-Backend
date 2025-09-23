from django.contrib import admin
from .models import CustomUser, Rol

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id","username","document_id","email","is_active","is_staff")
    search_fields = ("username","document_id","email")

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id","user","group_name","unidad")
    list_filter = ("group_name",)
    search_fields = ("user__username","user__document_id")
