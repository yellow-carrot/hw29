from django.http import JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.models import Category, Ad, Compilation
from ads.permissions import IsOwner, IsStuff
from ads.serializers import AdSerializer, CompilationSerializer, CompilationListSerializer, CompilationCreateSerializer, \
    CompilationRetrieveSerializer, CategorySerializer, AdCreateSerializer


# Create your views here.

class StatusView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"}, status=200)


# =========================Category_Views=======================

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# =========================Ad_Views=======================


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    default_serializer_class = AdSerializer

    default_permission = [AllowAny]

    permissions = {
        "retrieve": [IsAuthenticated],
        "create": [IsAuthenticated],
        "update": [IsAuthenticated, IsStuff | IsOwner],
        "partial_update": [IsAuthenticated, IsStuff | IsOwner],
        "destroy": [IsAuthenticated, IsStuff | IsOwner]
    }

    serializers = {
        "create": AdCreateSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer_class)

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
