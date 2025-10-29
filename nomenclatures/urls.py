from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AreaViewset

router = SimpleRouter()

router.register(r'areas', AreaViewset)

urlpatterns = [] + router.urls
