
from django.contrib import admin
from .models import User, Chat

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'tokens')
    search_fields = ('username',)

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('username', 'message', 'response', 'timestamp')
    search_fields = ('user__username', 'message')
    list_filter = ('timestamp',)
    
    def username(self, obj):
        return obj.user.username
    username.short_description = 'Username'
