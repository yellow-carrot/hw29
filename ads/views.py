import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad
from ads.serializers import AdSerializer
from hw29 import settings
from users.models import User


# Create your views here.

class StatusView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


# =========================Category_Views=======================
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by("name")

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


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    serializer_class = AdSerializer

    def list(self, request, *args, **kwargs):
        cat = request.GET.getlist('cat', None)
        if cat:
            self.queryset = self.queryset.filter(category_id__in=cat)

        text = request.GET.get('text', None)
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location', None)
        if location:
            self.queryset = self.queryset.filter(author_id__location_id__name__icontains=location)

        price_from = request.GET.get('price_from', None)
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get('price_to', None)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)

# class AdListView(ListView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#
#         self.object_list = self.object_list.order_by("-price")
#
#         paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#
#         ads = []
#
#         for ad in self.object_list:
#             ads.append({
#                 "id": ad.id,
#                 "name": ad.name,
#                 "author": ad.author_id.username,
#                 "price": ad.price
#             })
#
#         response = {
#             "items": ads,
#             "num_pages": page_obj.paginator.num_pages,
#             "total": page_obj.paginator.count,
#         }
#         return JsonResponse(response, safe=False, status=200)
#
#
# class AdDetailView(DetailView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         ad = self.get_object()
#
#         response = {
#             "id": ad.id,
#             "name": ad.name,
#             "author_id": ad.author_id.id,
#             "author": ad.author_id.username,
#             "price": ad.price,
#             "description": ad.description,
#             "is_published": ad.is_published,
#             "category_id": ad.category_id.id,
#             "image": ad.image.url,
#         }
#
#         return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdCreateView(CreateView):
#     model = Ad
#     fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']
#
#     def post(self, request, *args, **kwargs):
#         ad_data = json.loads(request.body)
#
#         ad = Ad.objects.create(
#             id=ad_data['id'],
#             name=ad_data['name'],
#             price=ad_data['price'],
#             description=ad_data['description'],
#             is_published=ad_data['is_published'],
#             image=ad_data['image'],
#             author_id=get_object_or_404(User, pk=ad_data['author_id']),
#             category_id=get_object_or_404(Category, pk=ad_data['category_id'])
#         )
#
#         return JsonResponse({
#             "id": ad.id,
#             "name": ad.name,
#             "author": ad.author_id.username,
#         })
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdUpdateView(UpdateView):
#     model = Ad
#     fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']
#
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#
#         ad_data = json.loads(request.body)
#         self.object.name = ad_data["name"]
#         self.object.author_id = get_object_or_404(User, pk=ad_data['author_id'])
#         self.object.price = ad_data["price"]
#         self.object.description = ad_data["description"]
#         self.object.is_published = ad_data["is_published"]
#         self.object.image = ad_data["image"]
#         self.object.category_id = get_object_or_404(Category, pk=ad_data['category_id'])
#
#         try:
#             self.object.full_clean()
#         except ValidationError as e:
#             return JsonResponse(e.message_dict, status=422)
#
#         self.object.save()
#         response = {
#             "id": self.object.id,
#             "name": self.object.name,
#             "author": self.object.author_id.username,
#         }
#         return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#         super().delete(request, *args, **kwargs)
#
#         return JsonResponse({"status": "ok"}, status=200)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AdImageView(UpdateView):
#     model = Ad
#     fields = ['name', 'author_id', 'price', 'description', 'is_published', 'image', 'category_id']
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         self.object.image = request.FILES.get("image")
#         self.object.save()
#
#         return JsonResponse({
#             "id": self.object.id,
#             "name": self.object.name,
#             "image": self.object.image.url
#         })
