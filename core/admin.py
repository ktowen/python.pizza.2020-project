from django.contrib import admin

from core.models import Libro, Autor, Articulo

admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Articulo)