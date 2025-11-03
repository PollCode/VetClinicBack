from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import AreaViewset, SpeciesViewset, BreedViewset

router = SimpleRouter()

router.register(r'areas', AreaViewset)
router.register(r'species', SpeciesViewset)
router.register(r'breeds', BreedViewset)

urlpatterns = [] + router.urls
