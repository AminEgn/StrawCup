# drf
from rest_framework import serializers

# internal
from apps.upload.models import Session


class SessionSerializer(serializers.ModelSerializer):
    """Session Serializer"""

    user = serializers.CurrentUserDefault()

    class Meta:
        model = Session
        fields = (
            "hash_serial",
            "chunked",
            "file_size",
            "created_at",
            "user",
        )
        read_only_fields = (
            "hash_serial",
        )
        extra_kwargs = {
            "user": {"required": False, "write_only": True},
        }
