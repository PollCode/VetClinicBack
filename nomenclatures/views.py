from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Area, Breed
from .serializers import (AreaSerializer, AreaCreateUpdateSerializer, 
                          BreedSerializer, BreedCreateUpdateSerializer)
from .perms import (HasViewAreaPermission, HasAddAreaPermission, HasChangeAreaPermission, HasDeleteAreaPermission,
                    HasViewBreedPermission, HasAddBreedPermission, HasChangeBreedPermission, HasDeleteBreedPermission)
from common.utils.auth import get_username_from_request


class AreaViewset(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AreaSerializer
        elif self.action == 'create' or 'partial_update' or 'update':
            return AreaCreateUpdateSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [HasViewAreaPermission(), IsAuthenticated()]
        elif self.action == 'create':
            return [HasAddAreaPermission(), IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [HasChangeAreaPermission(), IsAuthenticated()]
        elif self.action == 'destroy':
            return [HasDeleteAreaPermission(), IsAuthenticated()]
        return super().get_permissions()
    
    
    def list(self, request):
        areas = self.queryset.filter(deleted=False)
        serializer = self.get_serializer(areas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.queryset.get(id=pk), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            area = serializer.save(created_by=get_username_from_request(request))
            return Response(AreaSerializer(area).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        area = self.get_object()
        serializer = self.get_serializer(area, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_area = serializer.save(updated_by=get_username_from_request(request))
            return Response(AreaSerializer(updated_area).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            area = Area.objects.get(id=pk)
            area.deleted_by = get_username_from_request(request)
            area.deleted_date = timezone.now() 
            area.deleted = True
            area.save()
            return Response(status=status.HTTP_204_NO_CONTENT)    
        except Area.DoesNotExist:
            return Response({"detail": "Área no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        

    
    
class BreedViewset(viewsets.ModelViewSet):
    queryset = Breed.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return BreedSerializer
        elif self.action == 'create' or 'partial_update' or 'update':
            return BreedCreateUpdateSerializer
        return super().get_serializer_class()
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [HasViewBreedPermission(), IsAuthenticated()]
        elif self.action == 'create':
            return [HasAddBreedPermission(), IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [HasChangeBreedPermission(), IsAuthenticated()]
        elif self.action == 'destroy':
            return [HasDeleteBreedPermission(), IsAuthenticated()]
        return super().get_permissions()
    
    def list(self, request):
        breeds = self.queryset.filter(deleted=False)
        serializer = self.get_serializer(breeds, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.queryset.get(id=pk), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            breed = serializer.save(created_by=get_username_from_request(request))
            return Response(SpeciesSerializer(breed).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        breed = self.get_object()
        serializer = self.get_serializer(breed, data=request.data, partial=partial)
        if serializer.is_valid():
            updated_breed = serializer.save(updated_by=get_username_from_request(request))
            return Response(BreedSerializer(updated_breed).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        try:
            breed = Breed.objects.get(id=pk)
            breed.deleted_date = timezone.now() 
            breed.deleted_by = get_username_from_request(request)
            breed.deleted = True
            breed.save()
            return Response(status=status.HTTP_204_NO_CONTENT)    
        except Breed.DoesNotExist:
            return Response({"detail": "Raza no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        