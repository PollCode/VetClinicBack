from ..models.users import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['id'] = user.id
        token['username'] = user.username
        token['full_name'] = user.get_full_name  # Asegúrate de que esto sea un método o propiedad
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        token['rol'] = str(user.rol)  # __str__() es redundante; usa str()
        return token

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        # Validar existencia del usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "username": "La cuenta no existe."
            })

        # Verificar si la cuenta está activa
        if not user.is_active:
            raise serializers.ValidationError({
                "username": "La cuenta está suspendida."
            })
        # Autenticar credenciales
        if not user.check_password(password):
            raise serializers.ValidationError({
                "password": "Contraseña incorrecta."
            })

        # Si todo está bien, generar el token
        data = super().validate(data)

        # Agregar datos adicionales
        data.update({
            "user": {
                "id": user.id,
                "username": user.username,
                "full_name": user.get_full_name,
                "rol": str(user.rol)
            }
        })
        return data

        

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or has expired')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return super().validate(attrs)

    def save(self, **kwargs):

        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
