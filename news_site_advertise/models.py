from django.db import models
from django.utils.html import format_html
import os
import random


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    random_num = random.randint(1, 989999999)
    name, ext = get_filename_ext(filename)
    final_name = f"{random_num}-ad{ext}"
    return f"advertise/{final_name}"


class AdvertiseManager(models.Manager):
    def get_active_advertise(self):
        return self.get_queryset().filter(active=True)

    def get_header_advertise(self):
        return self.get('header_ad').filter(active=True)


class Advertise(models.Model):
    title_header_ad = models.CharField(max_length=200, default='عنوان تبلیغ هدر', verbose_name='عنوان تبلیغ هدر')
    link_header_ad = models.CharField(max_length=500, default='لینک تبلیغ هدر', verbose_name='لینک تبلیغ هدر')
    header_ad = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تبلیغ هدر')
    title_sidebar_ad_1 = models.CharField(max_length=200, default='عنوان سایدبار 1', verbose_name='عنوان سایدبار 1')
    link_sidebar_ad_1 = models.CharField(max_length=500, default='لینک تبلیغ 1', verbose_name='لینک تبلیغ 1')
    sidebar_ad_1 = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تبلیغ سایدبار 1')
    title_sidebar_ad_2 = models.CharField(max_length=200, default='عنوانسایدبار 2', verbose_name='عنوان سایدبار 2')
    link_sidebar_ad_2 = models.CharField(max_length=500, default='لینک تبلیغ 2', verbose_name='لینک تبلیغ 2')
    sidebar_ad_2 = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تبلیغ سایدبار 2')
    title_sidebar_ad_3 = models.CharField(max_length=200, default='عنوان سایدبار 3', verbose_name='عنوان سایدبار 3')
    link_sidebar_ad_3 = models.CharField(max_length=500, default='لینک تبلیغ 3', verbose_name='لینک تبلیغ 3')
    sidebar_ad_3 = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تبلیغ سایدبار 3')

    active = models.BooleanField(default=True, verbose_name="فعال / غیرفعال")

    objects = AdvertiseManager()

    class Meta:
        verbose_name = "تبلیغ"
        verbose_name_plural = "تبلیغات"

    def get_image_or_default_header_ad(self):
        try:
            return self.header_ad.url
        except:
            return '/static/default/news_default.jpg'

    def get_image_or_default_sidebar_ad_1(self):
        try:
            return self.sidebar_ad_1.url
        except:
            return '/static/default/news_default.jpg'

    def get_image_or_default_sidebar_ad_2(self):
        try:
            return self.sidebar_ad_2.url
        except:
            return '/static/default/news_default.jpg'

    def get_image_or_default_sidebar_ad_3(self):
        try:
            return self.sidebar_ad_3.url
        except:
            return '/static/default/news_default.jpg'

    def show_image_in_admin_header_ad(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(
                self.get_image_or_default_header_ad()))

    def show_image_in_admin_sidebar_ad_1(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(
                self.get_image_or_default_sidebar_ad_1()))

    def show_image_in_admin_sidebar_ad_2(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(
                self.get_image_or_default_sidebar_ad_2()))

    def show_image_in_admin_sidebar_ad_3(self):
        return format_html(
            "<img style='border-radius: 5px' width=120px height=85px  src='{}' >".format(
                self.get_image_or_default_sidebar_ad_3()))
