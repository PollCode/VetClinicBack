from django.urls import path
from rest_framework.routers import SimpleRouter
from .views.users import UserViewSet
from .views.auth import LoginUserView, LogoutUserView

router = SimpleRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
] + router.urls
