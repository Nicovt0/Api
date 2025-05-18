from django.db import models
from django.utils import timezone

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    rut = models.IntegerField()
    dv = models.CharField(max_length=1)
    nombre_empresa = models.CharField(max_length=100)
    pais_empresa = models.CharField(max_length=100)
    rut_empresa = models.IntegerField()
    puntuacion = models.FloatField()

class Marca(models.Model):
    id_marca = models.AutoField(primary_key=True)
    nombre_marca = models.CharField(max_length=100)

class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=100)

class Prod_Proveedor(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField()
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    id_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)

class Orden(models.Model):
    id_orden = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, default='pendiente')
    fecha = models.DateTimeField(default=timezone.now)

class ProductoOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Prod_Proveedor, on_delete=models.CASCADE)
    cantidad = models.IntegerField()