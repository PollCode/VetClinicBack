from django.conf import settings
from django.utils.crypto import get_random_string


RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


# class EncryptionText:

#     def __init__(self):
#         self._key = settings.ENCRYPTED_SECRET_KEY
#         self.cipher = Fernet(self._key)
#         self.encoder = 'utf-8'

#     def encrypt(self, text):
#         return self.cipher.encrypt(text.encode(self.encoder))

#     def decrypt(self, encrypted_text):
#         return self.cipher.decrypt(bytes(encrypted_text[2:-1], self.encoder)).decode(self.encoder)

#     def verify(self, text, encrypted_text):
#         return self.decrypt(encrypted_text) == text


class PasswordValidator:

    def __init__(
            self,
            min_length=8,
            min_length_digit=1,
            min_length_alpha=1,
            min_length_special=1,
            min_length_lower=1,
            min_length_upper=1,
            special_characters="~!@#$%^&*()_+{}\":;'[]",
    ):
        self.min_length = min_length
        self.min_length_digit = min_length_digit
        self.min_length_alpha = min_length_alpha
        self.min_length_special = min_length_special
        self.min_length_lower = min_length_lower
        self.min_length_upper = min_length_upper
        self.special_characters = special_characters

    def validate(self, password):
        validation_errors = []
        if len(password) < self.min_length:
            validation_errors.append(
                f'La contraseña debe contener al menos {self.min_length} caracteres.')

        if len([char for char in password if char.isdigit()]) < self.min_length_digit:
            validation_errors.append(
                f'La contraseña debe contener al menos {self.min_length_digit} dígito.')

        if len([char for char in password if char.isalpha()]) < self.min_length_alpha:
            validation_errors.append(
                f'La contraseña debe contener al menos {self.min_length_alpha} letras.')

        if len([char for char in password if char.isupper()]) < self.min_length_upper:
            validation_errors.append(
                f'La contraseña debe contener al menos {self.min_length_upper} mayúscula.')

        if len([char for char in password if char.islower()]) < self.min_length_lower:
            validation_errors.append(
                f'La contraseña debe contener al menos {self.min_length_lower} minúscula.')

        if len([char for char in password if char in self.special_characters]) < self.min_length_special:
            validation_errors.append(
                f'La contraseña debe contener al menos {self.min_length_special} caracter especial.')

        if validation_errors:
            return False, validation_errors
        return True, []

    def make_random_password(self):
        return get_random_string(length=self.min_length, allowed_chars=RANDOM_STRING_CHARS + self.special_characters)
