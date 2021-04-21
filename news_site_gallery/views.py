from django.http import Http404
from django.shortcuts import render
from .models import Gallery, ImageGallery
from django.views.generic import ListView


class GalleryList(ListView):
    def get_queryset(self):
        return Gallery.objects.get_publish_gallery()

    paginate_by = 12
    template_name = 'gallery/gallery_list.html'


def gallery_detail(request, *args, **kwargs):
    gallery_id = kwargs["GalleryId"]
    gallery = Gallery.objects.get_by_id(gallery_id)
    if gallery is None or not gallery.status == 'p':
        raise Http404("گالری مورد نظر یافت نشد")
    image_gallery = ImageGallery.objects.filter(gallery_id=gallery_id, status='p')

    context = {
        'gallery': gallery,
        'image_gallery': image_gallery
    }
    return render(request, 'gallery/gallery_detail.html', context)
