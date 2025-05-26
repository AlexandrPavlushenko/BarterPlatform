from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone",
        "avatar",
        "city",
        "is_active",
    )
    list_editable = ("is_active",)
    search_fields = ("email", "last_name")
