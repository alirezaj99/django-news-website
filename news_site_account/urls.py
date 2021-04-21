from django.contrib.auth import views
from django.urls import path
from .views import NewsList, NewsCreate, NewsUpdate, NewsDelete, ProfileUpdate, MaimNewsView, MaimNewsUpdate, \
    TagsCreate, TagsView, TagsUpdate, TagsDelete, Login, GalleryCreate, GalleryListView, GalleryUpdate, GalleryDelete, \
    ImageGalleryListView, ImageGalleryCreate, ImageGalleryUpdate, ImageGalleryDelete, SettingsUpdate, SettingsView, \
    NewsCommentView, NewsCommentUpdate, NewsCommentDelete, AdvertiseView, AdvertiseUpdate, NewsCategoryView, \
    NewsCategoryUpdate, NewsCategoryCreate, NewsCategoryDelete

app_name = "account"
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    #
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += [
    path('', NewsList.as_view(), name='home'),
    path('main-news/', MaimNewsView.as_view(), name='main_news'),
    path('main-news/update/<int:pk>/', MaimNewsUpdate.as_view(), name='main_news_update'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/comment/', NewsCommentView.as_view(), name='news_comment_list'),
    path('news/comment/update/<int:pk>/', NewsCommentUpdate.as_view(), name='news_comment_update'),
    path('news/comment/delete/<int:pk>/', NewsCommentDelete.as_view(), name='news_comment_delete'),
    path('news/update/<int:pk>/', NewsUpdate.as_view(), name='news_update'),
    path('news/delete/<int:pk>/', NewsDelete.as_view(), name='news_delete'),
    path('news/category/', NewsCategoryView.as_view(), name='news_category_list'),
    path('news/category/update/<int:pk>/', NewsCategoryUpdate.as_view(), name='news_category_update'),
    path('news/category/delete/<int:pk>/', NewsCategoryDelete.as_view(), name='news_category_delete'),
    path('news/category/create/', NewsCategoryCreate.as_view(), name='news_category_create'),
    path('profile/', ProfileUpdate.as_view(), name='profile'),
    path('tags/', TagsView.as_view(), name='tags_list'),
    path('tags/create/', TagsCreate.as_view(), name='tags_create'),
    path('tags/update/<int:pk>/', TagsUpdate.as_view(), name='tags_update'),
    path('tags/delete/<int:pk>/', TagsDelete.as_view(), name='tags_delete'),
    path('gallery/', GalleryListView.as_view(), name='gallery_list'),
    path('gallery/create/', GalleryCreate.as_view(), name='gallery_create'),
    path('gallery/update/<int:pk>/', GalleryUpdate.as_view(), name='gallery_update'),
    path('gallery/delete/<int:pk>/', GalleryDelete.as_view(), name='gallery_delete'),
    path('image-gallery/', ImageGalleryListView.as_view(), name='image_gallery_list'),
    path('image-gallery/create/', ImageGalleryCreate.as_view(), name='image_gallery_create'),
    path('image-gallery/update/<int:pk>/', ImageGalleryUpdate.as_view(), name='image_gallery_update'),
    path('image-gallery/delete/<int:pk>/', ImageGalleryDelete.as_view(), name='image_gallery_delete'),
    path('settings/', SettingsView.as_view(), name='settings_list'),
    path('settings/update/<int:pk>/', SettingsUpdate.as_view(), name='settings_update'),
    path('advertise/', AdvertiseView.as_view(), name='advertise_list'),
    path('advertise/update/<int:pk>/', AdvertiseUpdate.as_view(), name='advertise_update'),

]
