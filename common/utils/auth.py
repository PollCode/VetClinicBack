import jwt
import string
import random
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse


def get_token(request) -> str | None:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header:
            return None
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        return token

def decode_token(token:str)  -> tuple[dict | None, bool] :
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SIMPLE_JWT['ALGORITHM']])
        return payload, ''
    except jwt.ExpiredSignatureError:
        return None, 'Token expirado'
    except jwt.InvalidTokenError:
        return None, 'Token invalido'
    except Exception as e:
        return None, str(e)
    

def get_username_from_request(request):
    token = get_token(request)
    if token:
        decoded_token, error = decode_token(token)
        
        if not decoded_token:
            return JsonResponse({"detail": error}, status=status.HTTP_401_UNAUTHORIZED)
       
        return decoded_token.get("username", "")
         
    else:
        return None
    
def generar_contraseña():
    # Definir los conjuntos de caracteres
    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    especiales = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Asegurar al menos un carácter de cada tipo
    contraseña = [
        random.choice(mayusculas),
        random.choice(minusculas),
        random.choice(numeros),
        random.choice(especiales)
    ]
    
    # Rellenar el resto de la contraseña
    todos_caracteres = mayusculas + minusculas + numeros + especiales
    while len(contraseña) < 8:
        contraseña.append(random.choice(todos_caracteres))
    
    # Mezclar la lista para evitar que los primeros caracteres siempre sean del mismo tipo
    random.shuffle(contraseña)
    
    # Convertir la lista a string
    return ''.join(contraseña)