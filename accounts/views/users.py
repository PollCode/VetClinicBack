from rest_framework import viewsets
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.utils import timezone
from common.utils.auth import get_username_from_request, generar_contraseña
from ..serializers.users import UserSerializer, UserCreateSerializer, UserUpdateSerializer, PasswordChangeSerializer, ResetPasswordSerializer
from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from ..perms.users import HasViewUserPermission, HasAddUserPermission, HasChangeUserPermission, HasDeleteUserPermission, HasResetPasswordPermission


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return UserUpdateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [HasViewUserPermission(), IsAuthenticated()]
        elif self.action == 'create':
            return [HasAddUserPermission(), IsAuthenticated()]
        elif self.action == 'update' or self.action == 'partial_update':
            return [HasChangeUserPermission(), IsAuthenticated()]
        elif self.action == 'destroy':
            return [HasDeleteUserPermission(), IsAuthenticated()]
        return super().get_permissions()
        

    def list(self, request: Request):
        users = self.queryset.filter(is_active=True, )
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(created_by=get_username_from_request(request))
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request: Request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=partial)
        
        if serializer.is_valid(raise_exception=True):
            updated_user = serializer.save(updated_by=get_username_from_request(request))
            return Response(UserSerializer(updated_user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
             
    
    def retrieve(self, request: Request, pk=None):
        try:
            user = self.queryset.get(id=pk, is_active=True)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND) 
        
       

    def destroy(self, request: Request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.deleted_by = get_username_from_request(request)
            user.deleted_date = timezone.now()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated], url_path='change-password')
    def change_password(self, request):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password1'])
            user.save()
            # Cerrar otras sesiones activas (opcional) [[7]]
            update_session_auth_hash(request, user)
            return Response({"detail": "Contraseña actualizada con éxito"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['post'], permission_classes=[HasResetPasswordPermission], url_path='reset-password')
    def reset_password(self, request):
        serializer = ResetPasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data['username'])
            new_pwd = generar_contraseña()
            user.set_password(new_pwd)
            user.save()
            return Response({"new_password": new_pwd}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
