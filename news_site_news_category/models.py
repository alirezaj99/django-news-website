from django.db import models
from django.db.models import signals
from django.dispatch import dispatcher


class NewsCategoryManager(models.Manager):
    def get_active_category(self):
        return self.get_queryset().filter(active=True)


class NewsCategory(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.CASCADE,
                               related_name="children",
                               verbose_name="زیر دسته")
    title = models.CharField(max_length=150, verbose_name="عنوان دسته")
    name = models.CharField(max_length=150, verbose_name="عنوان در url")
    active = models.BooleanField(default=True, verbose_name="نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن", default=0)

    objects = NewsCategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی خبر"
        verbose_name_plural = "دسته بندی های اخبار"
        ordering = ['parent__id', 'position']

    def get_url(self):
        return f'/news/category/{self.name}'
