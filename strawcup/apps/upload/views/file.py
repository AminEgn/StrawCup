# drf
from rest_framework import status
from rest_framework import generics
from rest_framework import response
from rest_framework import exceptions

# internal
from apps.upload.models import FileType
from apps.upload.serializers import FileSerializer


class FileUploadView(generics.CreateAPIView):
    """File Upload View"""

    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("f", None) or request.FILES.get("file", None)
        if uploaded_file is None:
            message = "No file found, please specify 'f' or 'file' to upload."
            return response.Response(message, status=status.HTTP_400_BAD_REQUEST)

        if not hasattr(request, "content_type"):
            raise exceptions.NotAcceptable("content type not specified")

        content_length = request.headers.get("CONTENT_LENGTH", "")
        if not content_length or not content_length.isdecimal():
            raise exceptions.NotAcceptable("content len is wrong")

        if uploaded_file.size > 5242880:  # 5MB
            raise exceptions.NotAcceptable("use session upload to upload more than 5MB files")

        # print(physical.size, content_length)
        # if physical.size != int(content_length):
        #     print(physical.size - int(content_length))
        #     raise exceptions.NotAcceptable("content len is not same")

        # get or 415 unsupported media type
        file_type = FileType.objects.filter(
            mime_type=uploaded_file.content_type, is_active=True
        ).first()
        if file_type is None:
            raise exceptions.UnsupportedMediaType("not supported")

        request.data["f"] = uploaded_file
        request.data["file_type"] = file_type.id
        return super().post(request, *args, **kwargs)
