# dj
from django.utils import timezone
from django.db import transaction

# drf
from rest_framework import status
from rest_framework import response
from rest_framework import generics

# internal
from apps.upload.models import Session
from apps.upload.serializers import SessionSerializer


class SessionInitView(generics.CreateAPIView):
    """Session Init View"""

    serializer_class = SessionSerializer


class SessionUploadView(generics.GenericAPIView):
    """Session Upload View"""

    lookup_field = "hash_serial"
    # this filter has limited the queryset so the view's method
    # always returns 400 bad-request if the session not found
    # indeed the user has to what's happening to the session
    queryset = Session.objects.exclude(status=Session.Status.DELETED).select_related("file")
    serializer_class = None

    def put(self, request, *args, **kwargs):
        # the file name has to be equal to the content-type
        session = self.get_object()
        if not session.is_active:
            message = "Session is not active anymore"
            # this should be set as deleted
            session.status = Session.Status.DELETED
            session.save()
            return response.Response(message, status=status.HTTP_410_GONE)

        if session.status == Session.Status.COMPLETED:
            return response.Response(status.HTTP_201_CREATED)

        # this will save into temp folder (for Windows: C:\Users\SomeUser\AppData\Local\Temp\)
        # this level (TemporaryUploadFile) must skip and directly write in the file
        uploaded_file = request.FILES.get("f", None)
        # empty file with an empty content-range in header are required
        # but here we just check for file
        if uploaded_file is None:
            header_range = getattr(session.file, "size", 0)
            # if header_range is None:
            #     session.status = failed
            #     raise 404

            header_data = {
                "Content-Range": session.file_size,
                "Range": header_range
            }
            return response.Response(headers=header_data)

        file_session = session.file
        file_size = getattr(file_session, "size", 0)
        if file_size + uploaded_file.size <= session.file_size:
            # this view has to check for Content-Range to set offset of the pointer in file
            try:
                with transaction.atomic():
                    # this will raise PermissionError if file is locked
                    # to resolve this, File has to use Queue (FIFO)
                    file_session.append_chunk(uploaded_file)
                    session.last_used = timezone.now()

                    if session.status != Session.Status.PROCESSING:
                        session.status = Session.Status.PROCESSING

                    if file_session.size >= session.file_size:
                        session.status = Session.Status.COMPLETED

                    session.save()

            except Exception as e:
                session.status = Session.Status.FAILED
                session.save()
                print(e)
                message = {
                    "message": "Something goes wrong through the network please retry after a while",
                }
                return response.Response(message, status=status.HTTP_400_BAD_REQUEST)

            else:
                data = {
                    "status": session.status
                }
                return response.Response(data)

        # invalid last chunk
        message = "Chunk is not valid"
        return response.Response(message, status=status.HTTP_400_BAD_REQUEST)
