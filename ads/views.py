import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad
from hw27 import settings


# Create your views here.

class StatusView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


# =========================Category_Views=======================
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        categories = []

        for category in self.object_list:
            categories.append({
                "id": category.id,
                "name": category.name,
            })

        response = {
            "items": categories,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }
        return JsonResponse(response, safe=False, status=200)


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
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data['name'],
        )

        response = {
            "id": category.id,
            "name": category.name,
        }
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()
        response = {
            "id": self.object.id,
            "name": self.object.name,
        }
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


# =========================Ad_Views=======================

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
