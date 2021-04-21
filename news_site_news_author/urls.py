from django.urls import path
from .views import NewsListAuthor

app_name = "author"
urlpatterns = [
    path('author/<UserName>/', NewsListAuthor.as_view(), name="author_list"),
]
