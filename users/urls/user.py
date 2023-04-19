from django.urls import path

from users.views import UserListView, UserCreateView, UserRetrieveView, UserUpdateView, UserDestroyView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserRetrieveView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDestroyView.as_view()),
]
