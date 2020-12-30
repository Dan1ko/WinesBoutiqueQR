from django.shortcuts import render
from django.views import View


class DocsView(View):
    def get(self, request):
        # api_root_url = '206.189.51.3:8000'
        api_root_url = 'www.chapoutier.com'
        return render(request, 'docs/index.html', {'api_root_url': api_root_url})


class UserDocs(View):
    def get(self, request):
        # api_root_url = '206.189.51.3:8000'
        api_root_url = 'www.chapoutier.com'
        return render(request, 'docs/user.html', {'api_root_url': api_root_url})


class HorecaDocs(View):
    def get(self, request):
       # api_root_url = '206.189.51.3:8000'
        api_root_url = 'www.chapoutier.com'
        return render(request, 'docs/horeca.html', {'api_root_url': api_root_url})


class VinoDocs(View):
    def get(self, request):
       # api_root_url = '206.189.51.3:8000'
        api_root_url = 'www.chapoutier.com'
        return render(request, 'docs/vino.html', {'api_root_url': api_root_url})

