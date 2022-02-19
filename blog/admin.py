from django.contrib import admin
from .models import Tag, Post, Comment, Contact

# Registered models

class PostAdmin(admin.ModelAdmin):
    list_filter = ("user", "tags", "date")
    list_display = ("title", "date", "user")
    
class ContactAdmin(admin.ModelAdmin):
    list_filter = ("topic",)
    list_display = ("first_name","last_name","email", "topic")

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Contact, ContactAdmin)