from django.contrib import admin
from .models import Post, Category

admin.site.register(Category)


class PostAdmin(admin.ModelAdmin):
    last_display = ("title", "category", "created_on")
    last_filter = ("category",)
    search_fields = ["title", "keywords"]
    prepopulated_fields = {"slug": ('title',)}
# Register your models here.
admin.site.register(Post, PostAdmin)

