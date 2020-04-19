from django.db import models


class VersionesManager(models.Manager):
    def ultima(self):
        queryset = self.get_queryset()
        if queryset:
            return queryset.all()[0]
        else:
            return ''
