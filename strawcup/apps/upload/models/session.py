# std
import uuid
from datetime import timedelta

# dj
from django.db import models
from django.conf import settings
from django.utils import timezone


class Session(models.Model):
    """Session"""

    class Status(models.TextChoices):
        CREATED = "created"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"
        DELETED = "deleted"

    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.CREATED
    )
    hash_serial = models.CharField(max_length=70, unique=True, default=uuid.uuid4)
    # chunked default has to be True, because if not chunked uploading is selected
    # the file size maybe more than maximum size of the memory
    chunked = models.BooleanField(default=True)
    file_size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    last_used = models.DateTimeField(default=timezone.now)

    file = models.OneToOneField(
        "File", on_delete=models.CASCADE, related_name="session", null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions",
        # null and blank true has been set because there is no authentication for views
        null=True,
        blank=True
    )

    @property
    def is_active(self):
        # static seven days later
        seven_days = timedelta(days=7)
        if self.created_at + seven_days >= timezone.now():
            return True

        return False

    def __str__(self):
        return self.hash_serial
