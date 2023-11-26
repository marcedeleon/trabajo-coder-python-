from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class task(models.Model):
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo + '- creado por ' + self.usuario.username


class cliente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    telefono = models.IntegerField(blank=True)
    direccion = models.CharField(max_length=50)


class producto(models.Model):
    marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    codigo = models.IntegerField(blank=True)
    proveedor = models.CharField(max_length=50)
    stock = models.IntegerField(blank=False)


class articulo (models.Model):
    titulo = models.CharField(max_length=50, blank=True)
    subtitulo = models.CharField(max_length=50, blank=True)
    cuerpo = models.TextField(blank=True)
    autor = models.CharField(max_length=50, blank=True)
    fecha = models.DateField(auto_now=False, auto_now_add=False, blank=True)
