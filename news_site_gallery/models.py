from django.db import models
import random
import os
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from news_site_account.models import User
from extensions.utils import jalali_converter, jalali_converter_date


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 989999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{random_num}-{instance.title}{ext}"
    return f"gallery/{instance.title}/{final_name}"


class GalleryManager(models.Manager):
    def get_publish_gallery(self):
        return self.get_queryset().filter(status="p")

    def get_by_id(self, gallery_id):
        qs = self.get_queryset().filter(id=gallery_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None


class Gallery(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # publish
    )
    title = models.CharField(max_length=300, default="عنوان آلبوم", verbose_name="عنوان آلبوم")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="تصویر", blank=True, null=True)
    description = models.TextField(verbose_name='توضیحات گالری تصاویر', default='توضیحات گالری تصاویر')
    publish_time = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت آلبوم")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gallery", verbose_name="نویسنده")
    photographer = models.CharField(max_length=300, default="عکاس", verbose_name="عکاس")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="d", verbose_name="وضعیت انتشار")
    objects = GalleryManager()

    class Meta:
        verbose_name = "گالری"
        verbose_name_plural = "گالری ها"
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title

    def jtime(self):
        return jalali_converter(self.publish_time)

    jtime.short_description = "زمان انتشار"

    def jtime_date(self):
        return jalali_converter_date(self.publish_time)

    def get_absolute_url(self):
        return reverse("account:home")

    def show_image_in_admin(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(self.image.url))


class ImageGalleryManager(models.Manager):
    def get_active_image(self):
        return self.get_queryset().filter(status="p")


class ImageGallery(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # publish
    )
    title = models.CharField(max_length=300, verbose_name="عنوان")
    image = models.ImageField(upload_to=upload_image_path, verbose_name="تصویر")
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, verbose_name="گالری")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="image_gallery", verbose_name="نویسنده")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد تصویر")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default="p", verbose_name="وضعیت انتشار")

    objects = ImageGalleryManager()

    class Meta:
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"
        ordering = ["-create_time"]

    def __str__(self):
        return self.title

    def get_image_or_default(self):
        try:
            return self.image.url
        except:
            return '/static/default/news_default.jpg'

    def jtime(self):
        return jalali_converter(self.create_time)

    def show_image_in_admin(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(self.get_image_or_default()))
