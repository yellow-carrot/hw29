import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


# Create your views here.

class StatusView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        response = []

        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

    def post(self, request):
        data = json.loads(request.body)
        new_category = Category.objects.create(name=data.get("name"))
        return JsonResponse({"id": new_category.id, "name": new_category.name})


@method_decorator(csrf_exempt, name='dispatch')
class AdView(View):

    def get(self, request):
        ads = Ad.objects.all()
        response = []

        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price
            })

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False}, status=200)

    def post(self, request):
        data = json.loads(request.body)
        new_ad = Ad.objects.create(**data)

        return JsonResponse({
            "id": new_ad.id,
            "name": new_ad.name,
            "author": new_ad.author,
            "price": new_ad.price,
            "description": new_ad.description,
            "address": new_ad.address,
            "is_published": new_ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        response = {
            "id": category.id,
            "name": category.name
        }

        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        response = {
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        }

        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)
