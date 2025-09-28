from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models   

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Permet la connexion via email ou username
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
         
            user = UserModel.objects.get(
                models.Q(username__iexact=username) | models.Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
