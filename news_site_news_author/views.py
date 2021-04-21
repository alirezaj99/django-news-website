from django.shortcuts import render
from news_site_account.models import User
from django.views.generic import ListView
from django.http import Http404
from news_site_news.models import News


class NewsListAuthor(ListView):
    template_name = "news/news_list_author.html"
    paginate_by = 6

    def get_queryset(self):
        username = self.kwargs["UserName"]
        author = User.objects.filter(username__iexact=username, is_author=True).first()
        if author is None:
            raise Http404("صفحه ی مورد نظر یافت نشد")
        return News.objects.get_news_by_author(username).order_by("-time")

    def get_context_data(self, **kwargs):
        username = self.kwargs["UserName"]
        author = User.objects.filter(username__iexact=username, is_author=True).first()
        context = super().get_context_data(**kwargs)
        context["author"] = author

        return context
