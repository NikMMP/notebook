from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import upload, files_list, remove, download
from . import views
app_name = "files"

urlpatterns = [
    path('', files_list.as_view(), name='files'),
    path('upload/', upload.as_view(), name='upload'),
    path('view/<int:file_id>', views.detail, name='detail'),
    path('edit/<int:file_id>', views.edit, name='edit'),
    path('remove/<int:file_id>', remove.as_view(), name='remove'),
    path('download/<int:file_id>', download.as_view(), name='download'),
    path('show/<int:file_id>', views.show, name='show'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
