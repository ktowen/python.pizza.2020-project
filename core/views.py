from django.db.models import Count, Sum, OuterRef, IntegerField, Subquery
from django.shortcuts import render

from core import models
from core.utils.db import SubqueryCount, SubquerySum


def no(request):

    models.Autor.objects.all()

    models.Libro.objects.all()

    models.Articulo.objects.all()

    models.Autor.objects.annotate(
        precios_totales=Sum("libros__precio"),
    ).values("nombre", "precios_totales")

    models.Autor.objects.annotate(
        total_articulos=Count("articulos"),
    ).values("nombre", "total_articulos")

    models.Autor.objects.annotate(
        precios_totales=Sum("libros__precio"),
        total_articulos=Count("articulos"),
    ).values("nombre", "total_articulos", "precios_totales")

    models.Autor.objects.annotate(
        precios_totales=Sum("libros__precio"),
        total_articulos=Count("articulos"),
    ).order_by(
        "id",
        "libros__id",
        "articulos__id",
    ).values(
        "nombre",
        "articulos__nombre",
        "total_articulos",
        "libros__nombre",
        "precios_totales",
    )

    class SubqueryCount(Subquery):
        template = "(SELECT count(*) FROM (%(subquery)s) _count)"
        output_field = IntegerField()


    class SubquerySum(Subquery):
        template = "(SELECT sum(%(field)s) FROM (%(subquery)s) _sum)"


    class SubqueryMax(Subquery):
        template = "(SELECT max(%(field)s) FROM (%(subquery)s) _max)"


    models.Autor.objects.annotate(
        precios_totales=SubquerySum(
            models.Libro.objects.filter(autor=OuterRef("pk")),
            field="precio",
            output_field=IntegerField(),
        ),
        total_articulos=SubqueryCount(
            models.Articulo.objects.filter(autor=OuterRef("pk")),
            output_field=IntegerField(),
        ),
    ).values("nombre", "total_articulos", "precios_totales")


    SubqueryMax()


def index(request):
    queries = []
    queries.append(models.Autor.objects.values())
    queries.append(models.Libro.objects.values("id", "nombre", "autor", "precio"))
    queries.append(models.Articulo.objects.values("id", "nombre", "autor"))
    queries.append(
        models.Autor.objects.annotate(
            precios_totales=Sum("libros__precio"),
        ).values("nombre", "precios_totales")
    )
    queries.append(
        models.Autor.objects.annotate(
            total_articulos=Count("articulos"),
        ).values("nombre", "total_articulos")
    )
    queries.append(
        models.Autor.objects.annotate(
            precios_totales=Sum("libros__precio"),
            total_articulos=Count("articulos"),
        ).values("nombre", "total_articulos", "precios_totales")
    )
    queries.append(
        models.Autor.objects.annotate(
            precios_totales=Sum("libros__precio"),
            total_articulos=Count("articulos"),
        )
        .order_by("id", "libros__id", "articulos__id")
        .values(
            "nombre",
            "articulos__nombre",
            "total_articulos",
            "libros__nombre",
            "precios_totales",
        )
    )
    queries.append(
        models.Autor.objects.annotate(
            precios_totales=SubquerySum(
                models.Libro.objects.filter(autor=OuterRef("pk")),
                field="precio",
                output_field=IntegerField(),
            ),
            total_articulos=SubqueryCount(
                models.Articulo.objects.filter(autor=OuterRef("pk")),
                output_field=IntegerField(),
            ),
        ).values("nombre", "total_articulos", "precios_totales")
    )

    return render(request, "core/index.html", {"queries": queries})