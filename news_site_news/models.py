from django.db import models
from django.db.models.signals import pre_delete
from django.utils import timezone
from ckeditor.fields import RichTextField
from news_site_account.models import User
import random
import os
from django.urls import reverse
from django.utils.html import format_html
from extensions.utils import jalali_converter, jalali_converter_date
from news_site_news_category.models import NewsCategory
from news_site_news_tag.models import Tags
from django.db.models import Q
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
import uuid


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 989999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{random_num}-{instance.title}{ext}"
    return f"news/{final_name}"


class NewsManager(models.Manager):
    def get_publish_news(self):
        return self.get_queryset().filter(status="p")

    def get_news_by_id(self, news_id):
        qs = self.get_queryset().filter(id=news_id, status="p")
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def get_news_by_id_preview(self, news_id):
        qs = self.get_queryset().filter(id=news_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def get_news_by_category(self, category_name):
        return self.get_queryset().filter(categories__name__iexact=category_name, status="p")

    def get_news_by_author(self, username):
        return self.get_queryset().filter(author__username__iexact=username, status="p")

    def get_news_by_tag(self, tag_name):
        return self.get_queryset().filter(tags__slug__iexact=tag_name, status="p")

    def search(self, query):
        lookup = (Q(title__icontains=query) |
                  Q(description__icontains=query) |
                  Q(tags__title__icontains=query))
        return self.get_queryset().filter(lookup, status="p").distinct()


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="???? ???? ????????")
    time = models.DateTimeField(auto_now_add=True, verbose_name="???????? ??????")

    class Meta:
        verbose_name = "???? ???? ????????"
        verbose_name_plural = "???? ???? ???????? ????"

    def __str__(self):
        return self.ip_address

    def jtime(self):
        return jalali_converter(self.time)

    jtime.short_description = "???????? ??????"


class News(models.Model):
    STATUS_CHOICES = (
        ('d', '?????? ????????'),  # draft
        ('p', '?????????? ??????'),  # publish
        ('i', '?????????? ??????????'),  # investigation
        ('b', '?????????? ???????? ??????'),  # back
    )
    title = models.CharField(max_length=250, default="?????????? ??????", verbose_name="?????????? ??????")
    description = RichTextField(default="?????? ??????", verbose_name="?????? ??????")
    time = models.DateTimeField(default=timezone.now, verbose_name="???????? ????????????")
    updated = models.DateTimeField(auto_now=True, verbose_name="???????? ????????????????")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news", verbose_name="??????????????")
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True,
                              verbose_name="?????????? ????????")
    hits = models.ManyToManyField(IPAddress, blank=True, through="NewsHit", related_name="hits", verbose_name="??????????")
    categories = models.ManyToManyField(NewsCategory, blank=True, related_name="news_category",
                                        verbose_name="???????? ???????? ????")
    is_special = models.BooleanField(default=False, verbose_name="?????? ????????")
    tags = models.ManyToManyField(Tags, blank=True, related_name="news_tag",
                                  verbose_name="???? ???? / ?????????? ????")

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="d", verbose_name="?????????? ????????????")
    objects = NewsManager()

    class Meta:
        verbose_name = "??????"
        verbose_name_plural = "??????????"
        ordering = ["-time"]

    def __str__(self):
        return self.title

    def get_image_or_default(self):
        try:
            return self.image.url
        except:
            return '/static/default/news_default.jpg'

    def jtime(self):
        return jalali_converter(self.time)

    jtime.short_description = "???????? ????????????"

    def jtime_date(self):
        return jalali_converter_date(self.time)

    def get_absolute_url(self):
        return reverse("account:home")

    def get_url(self):
        return f"/news/{self.id}"

    def show_image_in_admin(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(self.get_image_or_default()))

    show_image_in_admin.short_description = "?????????? ??????????????????"

    def category_to_str(self):
        return " - ".join([category.title for category in self.categories.get_active_category()])

    category_to_str.short_description = "???????? ????????"


class NewsHit(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name="??????")
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE, verbose_name="???? ???? ????????")
    created = models.DateTimeField(auto_now_add=True, verbose_name="???????? ??????")

    class Meta:
        verbose_name = "?????????? ?????? ???? ???? ???????? ?? ??????????"
        verbose_name_plural = "?????????? ?????? ???? ???? ???????? ???? ?? ??????????????"

    def jtime(self):
        return jalali_converter(self.created)

    jtime.short_description = "???????? ??????"


class NewsCommentManager(models.Manager):
    def get_publish_comment(self, news_id):
        return self.get_queryset().filter(is_publish=True, news_id=news_id)


class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments", verbose_name="??????")
    name = models.CharField(max_length=200, verbose_name='??????')
    email = models.EmailField(max_length=120, verbose_name='??????????')
    web_site = models.CharField(max_length=120, verbose_name='???? ????????', default='website', blank=True)
    message = models.TextField(verbose_name='????????')
    time = models.DateTimeField(auto_now_add=True, verbose_name='?????????? ?????? ??????')
    is_publish = models.BooleanField(default=False, verbose_name='?????????? ????????????')

    objects = NewsCommentManager()

    class Meta:
        verbose_name = "??????"
        verbose_name_plural = "??????????"
        ordering = ['-time']

    def __str__(self):
        return str(self.news)

    def jtime(self):
        return jalali_converter(self.time)

    jtime.short_description = "???????? ????????????"

    def jtime_date(self):
        return jalali_converter_date(self.time)


@receiver(models.signals.post_delete, sender=News)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
