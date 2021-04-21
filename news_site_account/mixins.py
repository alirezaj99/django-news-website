from django.http import Http404
from django.shortcuts import get_object_or_404, redirect

from news_site_gallery.models import Gallery, ImageGallery
from news_site_news.models import News


class FieldMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ["title",
                           "description",
                           "time",
                           "author",
                           "image",
                           "categories",
                           "is_special",
                           "status",
                           "tags", ]
        elif request.user.is_author:
            self.fields = ["title",
                           "description",
                           "time",
                           "image",
                           "categories",
                           "is_special",
                           "tags",
                           ]

        else:
            raise Http404('این صفحه برای شما در دسترس نیست')

        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        news = get_object_or_404(News, pk=pk)
        if news.author == request.user and news.status in ["d", "b"] or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('این صفحه برای شما در دسترس نیست')


class SuperUserAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('این صفحه برای شما در دسترس نیست')


class SuperUserAndAuthorAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_author:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('account:profile')


class FormTagsValidMixin():
    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.active = True
        return super().form_valid(form)


class GalleryFieldMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title',
                           'image',
                           'publish_time',
                           'author',
                           'photographer',
                           'status',
                           'description', ]
        elif request.user.is_author:
            self.fields = ['title',
                           'image',
                           'publish_time',
                           'photographer',
                           'description',
                           ]

        else:
            raise Http404('این صفحه برای شما در دسترس نیست')

        return super().dispatch(request, *args, **kwargs)


class AuthorGalleryAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        gallery = get_object_or_404(Gallery, pk=pk)
        if gallery.author == request.user and gallery.status == "d" or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('این صفحه برای شما در دسترس نیست')


class ImageGalleryFieldMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['title',
                           'image',
                           'gallery',
                           'author',
                           'status', ]
        elif request.user.is_author:
            self.fields = ['title',
                           'image',
                           'gallery']

        else:
            raise Http404('این صفحه برای شما در دسترس نیست')

        return super().dispatch(request, *args, **kwargs)


class AuthorImageGalleryAccessMixin():
    def dispatch(self, request, pk, *args, **kwargs):
        image_gallery = get_object_or_404(ImageGallery, pk=pk)
        if image_gallery.author == request.user and image_gallery.status == "d" or \
                request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404('این صفحه برای شما در دسترس نیست')
