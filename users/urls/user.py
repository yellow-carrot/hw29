from django.urls import path

from users.views import UserListView, UserCreateView, UserUpdateView, UserRetrieveView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserRetrieveView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    # path('<int:pk>/delete/', UserDeleteView.as_view()),
]
