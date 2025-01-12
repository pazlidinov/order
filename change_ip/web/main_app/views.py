from django.http import JsonResponse
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.shortcuts import render

# Create your views here.


def homePageView(request):
    url = "https://"
    for key, value in request.GET.items():
        if key == "url":
            url = url + value + "&"
            continue
        url = url + key + "=" + value + "&"
    url = url[:-1]

    return render(request, "index.html", context={"url": url})

def upload_video(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        
        # Fayl nomini olish va saqlash joyini yaratish
        file_name = video_file.name
        file_path = os.path.join(settings.MEDIA_ROOT, 'videos', file_name)

        # Video faylni saqlash
        with default_storage.open(file_path, 'wb') as destination:
            for chunk in video_file.chunks():
                destination.write(chunk)

        return JsonResponse({'message': 'Video muvaffaqiyatli yuklandi!', 'file_path': file_path})

    return JsonResponse({'message': 'Fayl yuborilmadi!'}, status=400)