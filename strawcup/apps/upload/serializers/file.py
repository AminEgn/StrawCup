# drf
from rest_framework import serializers

# internal
from apps.upload.models import File


class FileSerializer(serializers.ModelSerializer):
    """File Serializer"""

    user = serializers.CurrentUserDefault()

    class Meta:
        model = File
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": False},
            "folder": {"required": False, "write_only": True},
            "file_type": {"write_only": True}
        }
