from django.contrib import admin
from .models.users import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'rol',
        'area',
    )
    readonly_fields = (
        'created_date',
        'created_by',
        'updated_date',
        'updated_by',
        'deleted_date',
        'deleted_by'
    )

admin.site.register(User, UserAdmin)