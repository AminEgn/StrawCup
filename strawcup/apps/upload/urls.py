# dj
from django.urls import path

# internal
from apps.upload import views


urlpatterns = [
    path("process", views.FileUploadView.as_view(), name="upload_process"),
    path("session_init", views.SessionInitView.as_view(), name="upload_session_init"),
    path(
        "session_process/<slug:hash_serial>",
        views.SessionUploadView.as_view(),
        name="upload_session_process"
    ),
]
