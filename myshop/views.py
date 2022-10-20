from django.shortcuts import render
from django.views import View


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class MapsView(View):
    def get(self, request):
        return render(request, 'products/maps.html')