import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet

from hw29 import settings
from users.models import User, Location
from users.serializers import LocationSerializer, UserListSerializer, UserRetrieveSerializer, UserCreateSerializer


# Create your views here.

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# ----------------------------------User_Views:-------------------------

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer






@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    #
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        #
        user_data = json.loads(request.body)
        self.object.first_name = user_data['first_name'],
        self.object.last_name = user_data['last_name'],
        self.object.username = user_data['username'],
        self.object.password = user_data['password'],
        self.object.role = user_data['role'],
        self.object.age = user_data['age']
        #

        for location in user_data['locations']:
            location_obj, _ = Location.objects.get_or_create(name=location)
            self.object.location_id.add(location_obj)
        #
        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)
        #
        self.object.save()
        response = {
            "id": self.object.id,
            "username": self.object.username
        }
        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)


#
#
@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
