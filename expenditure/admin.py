from django.contrib import admin
from .models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ["create_date", "title"]


admin.site.register(Post, PostAdmin)