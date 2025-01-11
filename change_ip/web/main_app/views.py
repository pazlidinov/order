from django.shortcuts import render

# Create your views here.

def homePageView(request):
    url=request.GET.get('url')    
    return render(request, 'index.html', context={'url':url})