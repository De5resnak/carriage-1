from django.contrib import admin
from .models import Message, GroupChat, UserProfile

class GroupChatAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)

admin.site.register(Message)
admin.site.register(GroupChat)
admin.site.register(UserProfile)