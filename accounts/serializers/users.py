from rest_framework import serializers
from ..models.users import User
from nomenclatures.serializers import AreaSerializer
from common.utils.passwords import PasswordValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    area = AreaSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'rol',
                  'area', 'is_superuser','is_active', )


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'password', 'rol', 'is_superuser', 'area']

    def validate(self, attrs):
        password = attrs.get('password')
        # Validar la contraseña (puedes usar tu lógica actual aquí)
        password_validator = PasswordValidator()
        is_valid, errors = password_validator.validate(password)
        if not is_valid:
            raise serializers.ValidationError({'password': errors})
        return attrs

    def create(self, validated_data):
        # Hash de la contraseña
        validated_data['password'] = make_password(validated_data['password'])
        # Crear el usuario
        user = super().create(validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'rol', 'is_superuser', 'area',]



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "La contraseña actual es incorrecta"})
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "Las nuevas contraseñas no coinciden"})
        validate_password(data['new_password1'], user=user) 
        return data
    

class ResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    admin_user = serializers.CharField(required=True)
    admin_password = serializers.CharField(required=True)
    
    def validate(self, data):
        try:
            user =User.objects.get(username=data['username'], is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "Usuario no encontrado"})
        
        try:
            admin_user = User.objects.get(username=data['admin_user'])
            admin_user_request = self.context['request'].user.username
            
            if not admin_user.username == admin_user_request:
                raise serializers.ValidationError({'admin_user': 'Este no es el usuario administrador que esta autenticado en la sesión'})
            
            if not admin_user.check_password(data['admin_password']):
                raise serializers.ValidationError({"admin_password": "Contraseña de administrador incorrecta"})
            
            return data
        
        except User.DoesNotExist:
            raise serializers.ValidationError({"admin_user": "Usuario no encontrado"})
            
             
        
