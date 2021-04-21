from django.db import models
import random
import os

from django.utils.html import format_html


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 989999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{random_num}-{instance.site_title}{ext}"
    return f"setting/site_logo/{final_name}"


class SettingsManager(models.Manager):
    def get_active_settings(self):
        return self.get_queryset().filter(active=True)


class Settings(models.Model):
    site_title = models.CharField(max_length=150, verbose_name='عنوان سایت', default='عنوان سایت')
    copyright = models.TextField(verbose_name='متن کپی رایت', default='متن کپی رایت')
    instagram = models.CharField(max_length=120, verbose_name='آیدی اینستاگرام', default='', blank=True)
    twitter = models.CharField(max_length=120, verbose_name='آیدی توییتر', default='', blank=True)
    facebook = models.CharField(max_length=120, verbose_name='آیدی فیسبوک', default='', blank=True)
    telegram = models.CharField(max_length=120, verbose_name='آیدی تلگرام', default='', blank=True)
    linkedin = models.CharField(max_length=120, verbose_name='آیدی لینکدین', default='', blank=True)
    youtube = models.CharField(max_length=120, verbose_name='آیدی یوتیوب', default='', blank=True)
    site_logo = models.ImageField(upload_to=upload_image_path, blank=True, null=True, verbose_name='لوگوسایت')
    site_logo_light = models.ImageField(upload_to=upload_image_path, blank=True, null=True,
                                        verbose_name='لوگوسایت روشن')
    site_icon = models.ImageField(upload_to=upload_image_path, blank=True, null=True, verbose_name='آیکون سایت در هدر')

    active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    objects = SettingsManager()

    def __str__(self):
        return self.site_title

    class Meta:
        verbose_name = 'تنظیم'
        verbose_name_plural = 'تنظیمات'
        ordering = ['-id']

    def get_image_or_default(self):
        try:
            return self.site_logo.url
        except:
            return '/static/default/news_default.jpg'

    def get_image_or_default_light(self):
        try:
            return self.site_logo_light.url
        except:
            return '/static/default/news_default.jpg'

    def get_image_or_default_icon(self):
        try:
            return self.site_icon.url
        except:
            return '/static/default/news_default.jpg'

    def show_image_in_admin(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=50px  src='{}' >".format(self.get_image_or_default()))

    def show_image_in_admin_light(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=50px  src='{}' >".format(
                self.get_image_or_default_light()))

    def show_image_in_admin_icon(self):
        return format_html(
            "<img style='border-radius: 5px' width=85px height=85px  src='{}' >".format(
                self.get_image_or_default_icon()))
