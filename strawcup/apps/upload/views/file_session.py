# drf
from rest_framework import generics

# internal
from apps.upload.models import Session
from apps.upload.serializers import SessionSerializer


class SessionInitView(generics.CreateAPIView):
    """Session Init View"""

    serializer_class = SessionSerializer


class SessionUploadView(generics.UpdateAPIView):
    """Session Upload View"""

    lookup_field = "hash_serial"
    # this filter has limited the queryset so the view's method
    # always returns 400 bad-request if the session not found
    # indeed the user has to what's happening to the session
    queryset = Session.objects.filter(
        status__in=(Session.Status.CREATED, Session.Status.PROCESSING)
    )

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
