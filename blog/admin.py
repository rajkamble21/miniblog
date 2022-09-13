from django.contrib import admin
from .models import Post, Category
# Register your models here.

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['id','img','title', 'category','desc']