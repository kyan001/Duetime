from django.db import models


class Notiecard(models.Model):
    title = models.CharField(max_length=30)
    kcol = models.CharField(max_length=30)
    vcol = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
