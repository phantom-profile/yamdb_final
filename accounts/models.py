from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', _('user')
        MODERATOR = 'moderator', _('moderator')
        ADMIN = 'admin', _('admin')

    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_(
        'about'), max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=Role.choices,
                            default=Role.USER)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['email']

    @property
    def token(self):
        return self.get_tokens_for_user()

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
        }

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
