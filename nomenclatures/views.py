from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Area
from .serializers import AreaSerializer, AreaCreateUpdateSerializer
from .perms import HasViewAreaPermission, HasAddAreaPermission, HasChangeAreaPermission, HasDeleteAreaPermission


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
        serializer = self.get_serializer(self.queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.queryset.get(id=pk), many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            area = serializer.save()
            return Response(AreaSerializer(area), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            area = serializer.save()
            return Response(AreaSerializer(area), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        area = get_object_or_404(Area, id=pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)