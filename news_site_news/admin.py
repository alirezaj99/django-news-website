from django.contrib import admin

from .models import News, IPAddress, NewsHit, NewsComment


class NewsAdmin(admin.ModelAdmin):
    list_display = ["__str__", "show_image_in_admin", "category_to_str", "jtime", "author", "is_special", "status"]
    list_editable = ["status"]
    search_fields = ["title", "description"]

    class meta:
        model = News


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ["__str__", "jtime"]

    class meta:
        model = IPAddress


class NewsHitAdmin(admin.ModelAdmin):
    list_display = ["jtime"]

    class meta:
        model = NewsHit


class NewsCommentAdmin(admin.ModelAdmin):
    list_display = ["__str__","name", "message", "email", "web_site", "is_publish"]
    list_editable = ["is_publish"]
    search_fields = ["news", "message", "web_site", "email"]
    list_filter = ["is_publish", "news"]

    class meta:
        model = NewsComment


admin.site.register(News, NewsAdmin)
admin.site.register(IPAddress, IPAddressAdmin)
admin.site.register(NewsHit, NewsHitAdmin)
admin.site.register(NewsComment, NewsCommentAdmin)
