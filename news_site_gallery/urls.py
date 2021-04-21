from django.urls import path
from .views import GalleryList, gallery_detail

app_name = "gallery"
urlpatterns = [
    path('', GalleryList.as_view(), name="gallery_list"),
    path('<GalleryId>/', gallery_detail, name="gallery_detail"),
]
