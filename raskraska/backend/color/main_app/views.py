from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

from .forms import PhotoForm

# Create your views here.


class HomePageView(TemplateView):
    template_name = "index.html"


class ImgPageView(TemplateView):
    template_name = "modified.html"


class ModifiedImgView(View):

    def post(self, request):
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            f = form.save(commit=False)
            uploaded_file = request.FILES["image"]
            f.title = uploaded_file.name
            f.modified_image = request.FILES["image"]
            f.save()           
            return redirect("main_app:img")
        return redirect("main_app:home")
