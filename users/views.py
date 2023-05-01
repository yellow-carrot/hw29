from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet

from users.models import User, Location
from users.serializers import LocationSerializer, UserListSerializer, UserRetrieveSerializer, UserCreateSerializer, \
    UserUpdateSerializer, UserDestroySerializer


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


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDestroyView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
