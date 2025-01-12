from django.urls import path

from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.homePageView, name='home'),
    path('upload/', views.upload_video, name='upload_video'),
]