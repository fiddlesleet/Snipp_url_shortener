from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, Http404
from django.views import View

from analytics.models import ClickEvent
from .forms import SubmitUrlForms
from .models import SnippURL


# Create your views here.

# class based views (CBVs)

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForms()
        bg_image = "http://miriadna.com/desctopwalls/images/max/Looking-at-the-tops-of-trees.jpg"
        context = {
            "title": "Snipp1.com",
            "form": the_form,
            "bg_image": bg_image
        }
        return render(request, "shortener/home.html", context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForms(request.POST)
        context = {
            "title": "Snipp1.com",
            "form": form,
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data.get("url")
            obj, created = SnippURL.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"
        return render(request, template, context)


class URLRedirectView(View):  # CBV = class-based view
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = SnippURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        return HttpResponseRedirect(obj.url)

# FBV and CBV's get method are virtually the same, but in CBVs must explicitly specify
#   the method you want to handle--eg get/post
# Also, CBVs more portable--we can move them around more easily than FBVs,
#   but they take longer to write


# def snipp_redirect_view(request, shortcode=None, *args, **kwargs):  # function based view

    # =================================================================
    # options if want to do something other than 404 error:
    # obj = SnippURL.objects.get(shortcode=shortcode)
    # try:
    #     obj = SnippURL.objects.get(shortcode=shortcode)
    # except:
    #     obj = SnippURL.objects.all().first()
    #
    # Good if you want some sort of default:
    # obj_url = None
    # qs = SnippURL.objects.filter(shortcode__iexact=shortcode.upper())
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()
    #     obj_url = obj.url
    # =================================================================

#    obj = get_object_or_404(SnippURL, shortcode=shortcode)
    # monitor clicks
#    return HttpResponseRedirect(obj.url)


