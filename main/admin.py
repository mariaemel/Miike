from django.contrib import admin
from .models import Publications, Comment

admin.site.register(Publications)

class PublicationsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_display_links = ('title', )
    ordering = ['title']
    list_per_page = 2
    actions = ['set_published', 'set_draft']


admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'datetime')
    search_fields = ('author', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)