import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Compilation
from ads.permissions import IsOwner
from ads.serializers import AdSerializer, CompilationSerializer, CompilationListSerializer, CompilationCreateSerializer, \
    CompilationRetrieveSerializer
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

    default_permission = [AllowAny]

    permissions = {
        "retrieve": [IsAuthenticated]
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

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


# =========================Compilation_Views=======================

class CompilationViewSet(ModelViewSet):
    queryset = Compilation.objects.order_by('name')
    default_serializer_class = CompilationSerializer

    default_permission = [AllowAny]

    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsOwner],
        "partial_update": [IsAuthenticated, IsOwner],
        "destroy": [IsAuthenticated, IsOwner]
    }

    serializers = {
        "list": CompilationListSerializer,
        "create": CompilationCreateSerializer,
        "retrieve": CompilationRetrieveSerializer
    }

    def get_permissions(self):
        return [permission() for permission in self.permissions.get(self.action, self.default_permission)]

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)
