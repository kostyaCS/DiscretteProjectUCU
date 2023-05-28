from django.contrib import admin
from .models import Message, UserProfile, MessageHistory

admin.site.register(Message)
admin.site.register(UserProfile)
admin.site.register(MessageHistory)