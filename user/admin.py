from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'address', 'github_link')
    list_filter = ('role', 'user__date_joined')
    search_fields = ('user__username', 'user__email', 'address')
    readonly_fields = ('user',)
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('role', 'profile_picture', 'address', 'github_link')
        }),
    )

admin.site.register(UserProfile, UserProfileAdmin)