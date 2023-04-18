import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from hw29 import settings
from users.models import User, Location


# Create your views here.

class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        # self.object_list = self.object_list.select_related('user').prefetch_related('location_id')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        users = []

        for user in self.object_list.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True))):
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "locations": [location.name for location in user.location_id.all()],
                "total_ads": user.total_ads
            })

        response = {
            "items": users,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }
        return JsonResponse(response, safe=False, status=200)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        response = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "locations": [location.name for location in user.location_id.all()],
        }

        return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, status=200)


#
@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    # location_id
    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age']
        )

        for location in user_data['locations']:
            location_obj, _ = Location.objects.get_or_create(name=location)
            user.location_id.add(location_obj)

        return JsonResponse({
            "id": user.id,
            "first_name": user.username,
            "locations": user.location_id.name,
        })


#
#
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
