from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView
from news_site_news.models import News
from news_site_news_category.models import NewsCategory
from .models import Tags


class NewsTag(ListView):
    template_name = "news/news_list_tag.html"
    paginate_by = 6

    def get_queryset(self):
        tag_name = self.kwargs["TagName"]
        tag = Tags.objects.filter(slug__iexact=tag_name).first()
        if tag is None:
            raise Http404("صفحه ی مورد نظر یافت نشد")
        return News.objects.get_news_by_tag(tag_name).order_by("-time")

    def get_context_data(self, **kwargs):
        tag_name = self.kwargs["TagName"]
        tag = Tags.objects.filter(slug__iexact=tag_name).first()
        context = super().get_context_data(**kwargs)
        context["tag"] = tag

        return context

