from django.db import models
from django.urls import reverse
from news_site_news.models import News


class MainNewsManager(models.Manager):
    def get_active_news(self):
        return self.get_queryset().filter(active=True)


class MainNews(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news", verbose_name="خبر اصلی بزرگ"
                             )
    news_1 = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_1", verbose_name="خبر اصلی کوچک 1"
                               )
    news_2 = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_2", verbose_name="خبر اصلی کوچک 2"
                               )
    news_3 = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_3", verbose_name="خبر اصلی کوچک 3"
                               )
    news_4 = models.ForeignKey(News, on_delete=models.CASCADE, related_name="news_4", verbose_name="خبر اصلی کوچک 4"
                               )

    active = models.BooleanField(default=True, verbose_name='وضعیت انتشار')

    objects = MainNewsManager()

    class Meta:
        verbose_name = "خبر اصلی در صفحه اصلی"
        verbose_name_plural = "اخبار اصلی در صفحه اصلی"

    def __str__(self):
        return self.news.title

    def get_absolute_url(self):
        return reverse("account:main_news")
