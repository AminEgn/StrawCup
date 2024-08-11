# std
import uuid

# dj
from django.core.files.base import ContentFile
from django.core.validators import RegexValidator

# drf
from rest_framework import serializers

# internal
from apps.upload.models import Session, File


class SessionSerializer(serializers.Serializer):
    """Session Serializer"""

    # user can specify the file's name.
    # it should validate with regex (it must be a name of a file with extension)
    name = serializers.CharField(
        max_length=255, write_only=True, validators=[RegexValidator("\w+[.]{1}[a-zA-Z]+")]
    )
    file_size = serializers.IntegerField()
    hash_serial = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    # user = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    def create(self, validated_data):
        name = validated_data.pop("name", "")
        # in session initialize, user has to fill file name
        hs = str(uuid.uuid4())
        validated_data["hash_serial"] = hs
        # user = validated_data["user"]
        # the user has to pass tp file object
        content_file = ContentFile(b"", name=name)
        f = File.objects.create(name=name, f=content_file)
        validated_data["file"] = f
        session = Session.objects.create(**validated_data)
        return session
