
from django.contrib import admin
from django.urls import path, include
from shortcourse import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortcourse_app.urls')),
    # path('edit_student_result/', EditResultViewClass.as_view(), name="edit_student_result"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
