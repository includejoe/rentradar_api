from django.contrib import admin

# Register your models here.
from django.contrib import admin

from . import models


# Register your models here.
class Conversation(admin.ModelAdmin):
    list_display = ("id", "created_at")


admin.site.register(models.Conversation, Conversation)


class Message(admin.ModelAdmin):
    list_display = ("id", "text", "attachment", "created_at")


admin.site.register(models.Message, Message)
