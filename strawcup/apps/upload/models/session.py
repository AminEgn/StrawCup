# dj
from django.db import models
from django.conf import settings


class Session(models.Model):
    """Session"""

    hash_serial = models.CharField(max_length=70, unique=True)
    chunked = models.BooleanField(default=False)
    file_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField()

    file = models.OneToOneField("File", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.hash_serial
