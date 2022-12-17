from django.contrib import admin
from django.contrib.admin import ModelAdmin

from base.models import Room, Message


class MessageAdmin(ModelAdmin):
    @staticmethod
    def cleanup_body(modeladmin, request, queryset):
        queryset.update(body="--- Deleted ---")

    ordering = ['id']
    list_display = ['id', 'body', 'room']
    list_display_links = ['id']
    list_per_page = 20
    list_filter = ['room']
    search_fields = ['body', 'id']
    actions = ['cleanup_body', 'body_short']

    fieldsets = [
        (
            None,
            {
                'fields': ['id', 'body']
            }
        ),
        (
            'Detail',
            {
                'fields': ['room', 'created', 'updated'],
                'description': 'Detailed information about room'
            }
        ),
        (
            'User information',
            {
                'fields': ['user']
            }
        )

    ]
    readonly_fields = ['id', 'created', 'updated']


class RoomAdmin(ModelAdmin):
    ordering = ['name']
    list_display = ['id', 'name', 'description']
    list_display_links = ['id', 'name']
    list_per_page = 20
    search_fields = ['name', 'description']

    fieldsets = [
        (
            None,
            {
                'fields': ['id', 'name', 'description']
            }
        ),
        (
            'Detail',
            {
                'fields': ['participants', 'created', 'updated'],
                'description': 'Detailed information about room'
            }
        ),

    ]
    readonly_fields = ['id', 'created', 'updated']


# Register your models here.
admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
