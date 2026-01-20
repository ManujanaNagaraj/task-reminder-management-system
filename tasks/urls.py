from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import TaskViewSet, UserRegistrationView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('', include(router.urls)),
]
