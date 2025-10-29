from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings  # til reference til Bruger

# -------------------
# Brugere-app
# -------------------

class BrugerManager(BaseUserManager):
    def create_user(self, brugernavn, adgangskode=None, **extra_fields):
        if not brugernavn:
            raise ValueError("Brugernavn skal udfyldes")
        user = self.model(brugernavn=brugernavn, **extra_fields)
        user.set_password(adgangskode)
        user.save(using=self._db)
        return user

    def create_superuser(self, brugernavn, adgangskode=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(brugernavn, adgangskode, **extra_fields)


class Rolle(models.Model):
    navn = models.CharField(max_length=50)
    rettigheder = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.navn


class Bruger(AbstractBaseUser, PermissionsMixin):
    brugernavn = models.CharField(max_length=100, unique=True)
    navn = models.CharField(max_length=100)
    rolle = models.ForeignKey(Rolle, on_delete=models.RESTRICT)
    afdeling = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BrugerManager()

    USERNAME_FIELD = 'brugernavn'
    REQUIRED_FIELDS = ['navn', 'rolle']

    def __str__(self):
        return self.brugernavn