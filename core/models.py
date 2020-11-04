from django.db import models


class Autor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["pk"]


class Libro(models.Model):
    nombre = models.CharField(max_length=300)
    precio = models.IntegerField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="libros")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["pk"]


class Articulo(models.Model):
    nombre = models.CharField(max_length=300)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="articulos")

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ["pk"]