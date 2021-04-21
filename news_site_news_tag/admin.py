from django.contrib import admin
from .models import Tags


class TagsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "slug", "active", "timestamp"]
    list_filter = ["active"]
    list_editable = ["active"]

    class meta:
        model = Tags


admin.site.register(Tags, TagsAdmin)
