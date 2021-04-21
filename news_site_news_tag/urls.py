from django.urls import path
from news_site_news_tag.views import NewsTag

app_name = "tags"
urlpatterns = [
    path('tag/<TagName>/', NewsTag.as_view(), name="news_list_tag"),
]
