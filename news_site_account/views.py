from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from news_site_news.models import News, NewsComment
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import FieldMixin, FormValidMixin, AuthorAccessMixin, SuperUserAccessMixin, FormTagsValidMixin, \
    SuperUserAndAuthorAccessMixin, GalleryFieldMixin, AuthorGalleryAccessMixin, ImageGalleryFieldMixin, \
    AuthorImageGalleryAccessMixin
from .models import User
from .forms import ProfileForm, MainNewsForm, TagsForm, SettingForm, NewsCommentForm, AdvertiseForm, NewsCategoryForm
from news_site_main_news_index.models import MainNews
from news_site_news_tag.models import Tags
from django.contrib.auth.views import LoginView
from news_site_gallery.models import Gallery, ImageGallery
from news_site_setting.models import Settings
from news_site_advertise.models import Advertise
from news_site_news_category.models import NewsCategory


class Login(LoginView):
    redirect_authenticated_user = reverse_lazy('account:home')

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')


class NewsList(LoginRequiredMixin, SuperUserAndAuthorAccessMixin, ListView):
    template_name = "registration/home.html"
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_superuser:
            return News.objects.all().order_by("-time")
        else:
            return News.objects.filter(author=self.request.user).order_by("-time")


class NewsCreate(LoginRequiredMixin, FieldMixin, FormValidMixin, CreateView):
    template_name = "registration/create_news_update.html"
    model = News


class NewsUpdate(AuthorAccessMixin, FieldMixin, FormValidMixin, UpdateView):
    template_name = "registration/create_news_update.html"
    model = News


class NewsDelete(SuperUserAccessMixin, DeleteView):
    model = News
    success_url = reverse_lazy('account:home')
    template_name = 'registration/news_confirm_delete.html'


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    template_name = "registration/profile.html"
    model = User
    success_url = reverse_lazy('account:profile')
    form_class = ProfileForm

    def get_object(self):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class MaimNewsView(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    template_name = 'registration/main_news.html'
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.is_superuser:
            return MainNews.objects.all()


class MaimNewsUpdate(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
    template_name = "registration/main_news_update.html"
    model = MainNews
    form_class = MainNewsForm

    def get_form_kwargs(self):
        kwargs = super(MaimNewsUpdate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class TagsView(LoginRequiredMixin, SuperUserAndAuthorAccessMixin, ListView):
    template_name = 'registration/tags.html'
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_author:
            return Tags.objects.all().order_by("-id")


class TagsCreate(SuperUserAndAuthorAccessMixin, FormTagsValidMixin, LoginRequiredMixin, CreateView):
    template_name = "registration/create_tag.html"
    model = Tags
    form_class = TagsForm

    def get_form_kwargs(self):
        kwargs = super(TagsCreate, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class TagsUpdate(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
    template_name = "registration/create_tag.html"
    model = Tags
    form_class = TagsForm


class TagsDelete(SuperUserAccessMixin, DeleteView):
    model = Tags
    success_url = reverse_lazy('account:tags_list')
    template_name = 'registration/tags_confirm_delete.html'


class GalleryCreate(LoginRequiredMixin, GalleryFieldMixin, FormValidMixin, CreateView):
    template_name = 'registration/create_gallery_update.html'
    model = Gallery
    success_url = reverse_lazy('account:gallery_list')


class GalleryListView(LoginRequiredMixin, SuperUserAndAuthorAccessMixin, ListView):
    template_name = "registration/gallery_list.html"
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Gallery.objects.all().order_by("-publish_time")
        else:
            return Gallery.objects.filter(author=self.request.user).order_by("-publish_time")


class GalleryUpdate(AuthorGalleryAccessMixin, GalleryFieldMixin, FormValidMixin, UpdateView):
    template_name = 'registration/create_gallery_update.html'
    model = Gallery
    success_url = reverse_lazy('account:gallery_list')


class GalleryDelete(SuperUserAccessMixin, DeleteView):
    model = Gallery
    success_url = reverse_lazy('account:gallery_list')
    template_name = 'registration/gallery_confirm_delete.html'


class ImageGalleryListView(LoginRequiredMixin, SuperUserAndAuthorAccessMixin, ListView):
    template_name = "registration/image_gallery_list.html"
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ImageGallery.objects.all().order_by("-create_time")
        else:
            return ImageGallery.objects.filter(author=self.request.user).order_by("-create_time")


class ImageGalleryCreate(LoginRequiredMixin, ImageGalleryFieldMixin, FormValidMixin, CreateView):
    template_name = 'registration/create_image_gallery_update.html'
    model = ImageGallery
    success_url = reverse_lazy('account:image_gallery_list')


class ImageGalleryUpdate(LoginRequiredMixin, AuthorImageGalleryAccessMixin, ImageGalleryFieldMixin, FormValidMixin,
                         UpdateView):
    template_name = 'registration/create_image_gallery_update.html'
    model = ImageGallery
    success_url = reverse_lazy('account:image_gallery_list')


class ImageGalleryDelete(LoginRequiredMixin, SuperUserAccessMixin, DeleteView):
    model = ImageGallery
    success_url = reverse_lazy('account:image_gallery_list')
    template_name = 'registration/image_gallery_confirm_delete.html'


class SettingsUpdate(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
    template_name = "registration/setting_update.html"
    model = Settings
    form_class = SettingForm
    success_url = reverse_lazy('account:settings_list')


class SettingsView(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    template_name = 'registration/setting_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Settings.objects.all().order_by("-id")


class NewsCommentView(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    template_name = 'registration/news_comment_list.html'
    paginate_by = 20

    def get_queryset(self):
        return NewsComment.objects.all().order_by("-time")


class NewsCommentUpdate(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
    template_name = 'registration/news_comment_update.html'
    model = NewsComment
    form_class = NewsCommentForm
    success_url = reverse_lazy('account:news_comment_list')


class NewsCommentDelete(SuperUserAccessMixin, DeleteView):
    model = NewsComment
    success_url = reverse_lazy('account:news_comment_list')
    template_name = 'registration/news_comment_confirm_delete.html'


class AdvertiseView(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    template_name = 'registration/advertise_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Advertise.objects.all().order_by("-id")


class AdvertiseUpdate(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
    template_name = 'registration/advertise_update.html'
    model = Advertise
    form_class = AdvertiseForm
    success_url = reverse_lazy('account:advertise_list')


class NewsCategoryView(LoginRequiredMixin, SuperUserAccessMixin, ListView):
    template_name = 'registration/news_category_list.html'
    paginate_by = 20

    def get_queryset(self):
        return NewsCategory.objects.all().order_by("-id")


class NewsCategoryUpdate(LoginRequiredMixin, SuperUserAccessMixin, UpdateView):
    template_name = 'registration/news_category_update.html'
    model = NewsCategory
    form_class = NewsCategoryForm
    success_url = reverse_lazy('account:news_category_list')


class NewsCategoryCreate(LoginRequiredMixin, SuperUserAccessMixin, CreateView):
    template_name = 'registration/news_category_update.html'
    model = NewsCategory
    success_url = reverse_lazy('account:news_category_list')
    form_class = NewsCategoryForm


class NewsCategoryDelete(LoginRequiredMixin, SuperUserAccessMixin, DeleteView):
    model = NewsCategory
    success_url = reverse_lazy('account:news_category_list')
    template_name = 'registration/news_category_confirm_delete.html'


def side_bar(request):
    setting = Settings.objects.get_active_settings().first()
    context = {
        'setting': setting
    }
    return render(request, 'registration/sidebar.html', context)

# انتقال بخش تنظیمات به ادمین شخصی ok
# اضاف کردن آیکون سایت ok
# اضاف کردن بخش نظرات به قالب ادمین شخصی ok
# اضاف کردن بخش تبلیغات به ////// ok
# دسته بندی اخبار ضروری نیست ok
