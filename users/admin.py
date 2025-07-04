from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Disable add and delete (handled by signals and models.CASCADE)
    def has_add_permission(self, request, obj = ...):
        return False

    def has_delete_permission(self, request, obj = ...):
        return False
