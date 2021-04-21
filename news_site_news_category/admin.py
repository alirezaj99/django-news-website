from django.contrib import admin
from .models import NewsCategory


class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["__str__", "name", "parent", "position", "active"]
    list_editable = ["active", "position"]

    class meta:
        model = NewsCategory


admin.site.register(NewsCategory, NewsCategoryAdmin)
