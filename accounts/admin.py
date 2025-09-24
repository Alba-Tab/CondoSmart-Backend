from django.contrib import admin
from .models import CustomUser, Rol

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("pk","username","ci","email","rol","is_active","is_staff")
    search_fields = ("username","ci","email")

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("pk","name")
    list_filter = ("name",)
    search_fields = ("user__username","user__ci")
