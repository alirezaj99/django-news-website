from django import forms

from news_site_advertise.models import Advertise
from news_site_news.models import NewsComment
from news_site_news_category.models import NewsCategory
from .models import User
from news_site_main_news_index.models import MainNews
from news_site_news_tag.models import Tags
from news_site_setting.models import Settings


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')

        super(ProfileForm, self).__init__(*args, **kwargs)

        if not user.is_superuser:
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True

        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'special_user',
            'is_author',
        ]


class MainNewsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(MainNewsForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['active'].disabled = True
        self.fields['news'].required = True
        self.fields['news_1'].required = True
        self.fields['news_2'].required = True
        self.fields['news_3'].required = True
        self.fields['news_4'].required = True

    class Meta:
        model = MainNews
        fields = [
            'news',
            'news_1',
            'news_2',
            'news_3',
            'news_4',
            'active',
        ]


class TagsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TagsForm, self).__init__(*args, **kwargs)
        if not user.is_superuser:
            self.fields['active'].disabled = True
        self.fields['title'].required = True
        self.fields['slug'].required = True

    class Meta:
        model = Tags
        fields = ['title', 'slug', 'active']


class SettingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SettingForm, self).__init__(*args, **kwargs)
        self.fields['site_title'].required = True
        self.fields['copyright'].required = True
        self.fields['site_logo'].required = True
        self.fields['site_logo_light'].required = True
        self.fields['site_icon'].required = True
        self.fields['active'].required = True

    class Meta:
        model = Settings
        fields = [
            'site_title',
            'copyright',
            'instagram',
            'twitter',
            'facebook',
            'telegram',
            'linkedin',
            'youtube',
            'site_logo',
            'site_logo_light',
            'site_icon',
            'active',
        ]


class NewsCommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsCommentForm, self).__init__(*args, **kwargs)
        self.fields['news'].required = True
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['message'].required = True

    class Meta:
        model = NewsComment
        fields = [
            'news',
            'name',
            'email',
            'message',
            'is_publish',
        ]


class AdvertiseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AdvertiseForm, self).__init__(*args, **kwargs)
        self.fields['title_header_ad'].required = False
        self.fields['header_ad'].required = False
        self.fields['title_sidebar_ad_1'].required = False
        self.fields['sidebar_ad_1'].required = False
        self.fields['title_sidebar_ad_2'].required = False
        self.fields['sidebar_ad_2'].required = False
        self.fields['title_sidebar_ad_3'].required = False
        self.fields['sidebar_ad_3'].required = False
        self.fields['active'].required = False
        self.fields['link_header_ad'].required = False
        self.fields['link_sidebar_ad_1'].required = False
        self.fields['link_sidebar_ad_2'].required = False
        self.fields['link_sidebar_ad_3'].required = False

    class Meta:
        model = Advertise
        fields = [
            'title_header_ad',
            'header_ad',
            'title_sidebar_ad_1',
            'sidebar_ad_1',
            'title_sidebar_ad_2',
            'sidebar_ad_2',
            'title_sidebar_ad_3',
            'sidebar_ad_3',
            'active',
            'link_header_ad',
            'link_sidebar_ad_1',
            'link_sidebar_ad_2',
            'link_sidebar_ad_3',
        ]


class NewsCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsCategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['name'].required = True
        self.fields['parent'].required = False
        self.fields['active'].required = False
        self.fields['position'].required = False

    class Meta:
        model = NewsCategory
        fields = [
            'parent',
            'title',
            'name',
            'active',
            'position',
        ]
