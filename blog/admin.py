from django.contrib import admin
from django.contrib.auth.hashers import make_password

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "private", "created_at"]
    list_filter = ["private"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "content")}),
        ("Privacy", {"fields": ("private", "password")}),
    )

    def save_model(self, request, obj, form, change):
        if "password" in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
