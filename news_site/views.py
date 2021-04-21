from django.db.models import Count, Q
from django.http import Http404
from django.shortcuts import render, redirect

from news_site_gallery.models import Gallery
from news_site_news.models import News, NewsComment
from django.core.paginator import Paginator
from news_site_news_category.models import NewsCategory
from datetime import datetime, timedelta
from extensions.utils import jalali_converter_date
from news_site_main_news_index.models import MainNews
from news_site_advertise.models import Advertise
from news_site_setting.models import Settings

def view_404(request, exception):
    context = {

    }
    return render(request, "shared/404.html", context)


def view_403(request, exception):
    context = {

    }
    return render(request, "shared/403.html", context)


def view_400(request, exception):
    context = {

    }
    return render(request, "shared/400.html", context)


def view_500(request):
    context = {

    }
    return render(request, "shared/500.html", context)


def home_page(request):
    news = News.objects.get_publish_news().order_by("-time")[:10]
    setting = Settings.objects.get_active_settings().first()

    context = {
        "page_obj": news,
        "setting": setting
    }
    return render(request, "index.html", context)


date = datetime.today()
jalali_date = jalali_converter_date(date)


def header(request):
    date = datetime.today()
    jalali_date = jalali_converter_date(date)
    time = datetime.today()
    advertise = Advertise.objects.get_active_advertise().first()
    setting = Settings.objects.get_active_settings().first()
    context = {
        'date': jalali_date,
        'time': time,
        'ad': advertise,
        'setting': setting
    }
    return render(request, "shared/Header.html", context)


def footer(request):
    most_visit_news = News.objects.get_publish_news().annotate(
        count=Count('hits')
    ).order_by('-count', '-time')[:3]
    categories = NewsCategory.objects.get_active_category().order_by("-position")
    setting = Settings.objects.get_active_settings().first()
    gallery = Gallery.objects.get_publish_gallery()[:6]
    context = {
        'setting': setting,
        'news': most_visit_news,
        'categories': categories,
        'galleries': gallery
    }
    return render(request, "shared/Footer.html", context)


def menu_category_partial(request):
    categories = NewsCategory.objects.get_active_category().order_by("-position")
    context = {
        "categories": categories
    }
    return render(request, "shared/menu_category_partial.html", context)


def sidebar(request):
    last_month = datetime.today() - timedelta(days=30)
    most_visit_news = News.objects.get_publish_news().annotate(
        count=Count('hits', filter=Q(newshit__created__gt=last_month))
    ).order_by('-count', '-time')[:6]
    categories = NewsCategory.objects.get_active_category().order_by("-position")
    news = News.objects.get_publish_news().order_by("-time")[:6]
    advertise = Advertise.objects.get_active_advertise().first()
    setting = Settings.objects.get_active_settings().first()

    context = {
        "categories": categories,
        "news": news,
        "most_visit_news": most_visit_news,
        "ad": advertise,
        'setting': setting
    }
    return render(request, "shared/_Sidebar.html", context)


def main_news(request):
    main_news = MainNews.objects.get_active_news().first()

    context = {
        'main_news': main_news
    }
    return render(request, "shared/MainNews.html", context)


def hot_news(request):
    news = News.objects.get_publish_news().order_by("-time")
    context = {
        'news': news
    }
    return render(request, "shared/_HotNews.html", context)


def header_references(request):
    setting = Settings.objects.get_active_settings().first()
    context = {
        'setting': setting
    }
    return render(request, "shared/_HeaderReferences.html", context)


def footer_references(request):
    context = {

    }
    return render(request, "shared/_FooterReferences.html", context)


def most_visit_last_day(request):
    last_day = datetime.today() - timedelta(days=1)
    most_visit_news = News.objects.get_publish_news().annotate(
        count=Count('hits', filter=Q(newshit__created__gt=last_day))
    ).order_by('-count', '-time')[:8]
    context = {
        'most_visit_last_day': most_visit_news
    }
    return render(request, "shared/most_visit_last_day.html", context)


def script_logo(request):
    setting = Settings.objects.get_active_settings().first()
    context = {
        'setting': setting
    }
    return render(request, "shared/script_logo.html", context)
