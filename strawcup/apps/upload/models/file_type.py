# dj
from django.db import models


class FileType(models.Model):
    """File Type"""

    extension = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=110)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.extension
