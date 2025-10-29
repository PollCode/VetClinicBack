from ..serializers.auth import LoginSerializer, LogoutSerializer
from ..models.users import User
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed


class LoginUserView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            # Generar respuesta personalizada
            response_data = {
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'user': serializer.validated_data['user']
            }

            return Response(response_data, status=status.HTTP_200_OK)
            
        except TokenError as e:
            raise InvalidToken(e.args[0])

        


class LogoutUserView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
