from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UsuarioManager(BaseUserManager):

    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("CPF é obrigatório")

        if not email:
            raise ValueError("Email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(cpf, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):

    class Genero(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMININO = "F", "Feminino"
        OUTRO = "O", "Outro"
        NAO_INFORMAR = "N", "Prefiro não informar"

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=1, choices=Genero.choices, default=Genero.NAO_INFORMAR)
    is_produtor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.nome