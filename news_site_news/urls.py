from django.urls import path
from .views import NewsList, news_detail, NewsListCategory, news_preview, SearchNews

app_name = "news"
urlpatterns = [
    path('news/', NewsList.as_view(), name="news_list"),
    path('news/category/<CategoryName>/', NewsListCategory.as_view(), name="news_list_category"),
    # path('news/<NewsId>/<name>', news_detail, name="news_detail"),
    path('news/<NewsId>/', news_detail, name="news_detail"),
    path('search/news/', SearchNews.as_view(), name="news_search"),
    path('preview/<NewsId>/', news_preview, name="news_preview"),
]
