from django.contrib import admin
from main.models import *


# admin.site.register(CardnoteCard)
@admin.register(CardnoteCard)
class CardnoteCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'user', 'title', 'kcol', 'vcol', 'category', 'created', 'modified')
    search_fields = ('title', 'kcol', 'vcol')
    list_filter = ('userid', 'category')
    date_hierarchy = 'modified'


# admin.site.register(CardnoteItem)
@admin.register(CardnoteItem)
class CardnoteItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cardnotecardid', 'kword', 'val', 'created', 'modified')
    search_fields = ('kword', 'val')
    date_hierarchy = 'modified'


# admin.site.register(ShortUrl)
@admin.register(ShortUrl)
class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'user', 'pv', 'name', 'url', 'created', 'modified')
    search_fields = ('name', 'url', 'user')
    list_filter = ('userid',)
    date_hierarchy = 'created'
