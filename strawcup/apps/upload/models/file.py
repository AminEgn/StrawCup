# std
from os import path
from hashlib import sha1

# dj
from django.db import models
from django.conf import settings


def get_upload_to(instance, filename):
    username = "username"
    if instance.user is not None:
        username = instance.user.username

    username_hash = sha1(username.encode()).hexdigest()
    return f"{username_hash}/{filename}"


class File(models.Model):
    """File"""

    name = models.CharField(max_length=255)
    f = models.FileField(upload_to=get_upload_to)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    file_type = models.ForeignKey("FileType", on_delete=models.RESTRICT, related_name="files")
    folder = models.ForeignKey(
        "Folder",
        on_delete=models.RESTRICT,
        related_name="files",
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="files",
        null=True,
        blank=True
    )

    @property
    def size(self):
        return self.f.size

    @property
    def url(self):
        return self.f.url

    @property
    def basename(self):
        return path.basename(self.f.name)

    @property
    def stem(self):
        return path.splitext(self.basename)[0]

    @property
    def extension(self):
        return path.splitext(self.basename)[1].lower()

    def _pre_save(self):
        self.name = self.name or self.stem

    def _post_save(self):
        pass

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self._pre_save()
        super().save(force_insert, force_update, using, update_fields)
        self._post_save()
