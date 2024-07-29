# dj
from django.db import models
from django.conf import settings


class Folder(models.Model):
    """Folder"""

    class Meta:
        unique_together = ["name", "user"]

    name = models.CharField(max_length=100)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="folders",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
