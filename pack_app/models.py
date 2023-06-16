from django.db import models
import os
class Batch(models.Model):
    plik = models.FileField(null=True)

