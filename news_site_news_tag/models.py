from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.urls import reverse


class TagsManager(models.Manager):
    def get_active_tag(self):
        return self.get_queryset().filter(active=True)


class Tags(models.Model):
    title = models.CharField(max_length=120, verbose_name="عنوان")
    slug = models.SlugField(verbose_name="عنوان در url", unique=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    active = models.BooleanField(default=True, verbose_name="فعال / غیرفعال")
    objects = TagsManager()

    class Meta:
        verbose_name = "برچسب / تگ"
        verbose_name_plural = "پرچسب ها / تگ ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("account:tags_list")


def tags_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tags_pre_save_receiver, sender=Tags)
