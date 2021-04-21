from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from news_site_news.models import News, NewsComment
from news_site_news_category.models import NewsCategory
from .forms import CommentCreateForm
from django.urls import reverse_lazy, reverse


class NewsList(ListView):
    template_name = "news/news_list.html"
    paginate_by = 12

    def get_queryset(self):
        return News.objects.get_publish_news().order_by("-time")


class NewsListCategory(ListView):
    template_name = "news/news_list.html"
    paginate_by = 12

    def get_queryset(self):
        category_name = self.kwargs["CategoryName"]
        category = NewsCategory.objects.filter(name__iexact=category_name).first()
        if category is None:
            raise Http404("صفحه ی مورد نظر یافت نشد")
        return News.objects.get_news_by_category(category_name).order_by("-time")

    def get_context_data(self, **kwargs):
        category_name = self.kwargs["CategoryName"]
        category = NewsCategory.objects.filter(name__iexact=category_name).first()
        context = super().get_context_data(**kwargs)
        context["category"] = category

        return context


class SearchNews(ListView):
    template_name = "news/news_list.html"
    paginate_by = 12

    def get_queryset(self):
        request = self.request
        query = request.GET.get("q")
        if query is not None:
            return News.objects.search(query).order_by("-time")
        return News.objects.get_publish_news().order_by("-time")


def news_detail(request, *args, **kwargs):
    news_id = kwargs["NewsId"]
    previous_news_id = int(news_id) - 1
    next_news_id = int(news_id) + 1
    str_previous = str(previous_news_id)
    str_next = str(next_news_id)
    news = News.objects.get_news_by_id(news_id)
    previous_news = News.objects.get_news_by_id(str_previous)
    next_news = News.objects.get_news_by_id(str_next)
    if news is None:
        raise Http404("خبر مورد نطر یافت نشد")
    ip_address = request.user.ip_address
    print(ip_address)
    if ip_address not in news.hits.all():
        news.hits.add(ip_address)

    comment: NewsComment = NewsComment.objects.get_publish_comment(news_id)
    comment_count = len(comment)
    comment_form = CommentCreateForm(request.POST or None)
    if comment_form.is_valid():
        name = comment_form.cleaned_data.get("name")
        web_site = comment_form.cleaned_data.get("web_site")
        message = comment_form.cleaned_data.get("message")
        email = comment_form.cleaned_data.get("email")
        NewsComment.objects.create(name=name, message=message, web_site=web_site, email=email, news_id=news_id)
        return HttpResponseRedirect(news.get_url())

    context = {
        "news": news,
        "form": comment_form,
        "comment": comment,
        "comment_count": comment_count,
        'previous_news': previous_news,
        'next_news': next_news

    }
    return render(request, "news/news_detail.html", context)


def news_preview(request, *args, **kwargs):
    news_id = kwargs["NewsId"]
    news = News.objects.get_news_by_id_preview(news_id)
    if news is None:
        raise Http404("خبر مورد نطر یافت نشد")
    context = {
    }

    if news.author == request.user and news.status in ["d", "b"] or \
            request.user.is_superuser:
        context["news"] = news
    else:
        raise Http404("صفحه مورد نطر یافت نشد")

    return render(request, "news/news_detail.html", context)
