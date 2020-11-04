from django.db import models


class SubqueryCount(models.Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()


class SubquerySum(models.Subquery):
    template = "(SELECT sum(%(field)s) FROM (%(subquery)s) _sum)"


class SubqueryMax(models.Subquery):
    template = "(SELECT max(%(field)s) FROM (%(subquery)s) _max)"
