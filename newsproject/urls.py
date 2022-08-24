from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from newsapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", views.home, name="home"),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
