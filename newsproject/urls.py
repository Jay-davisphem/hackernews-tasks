from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from newsapp import views, tasks, utils

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("newsapp.urls")),
    path("api/", include("newsapi.urls"), name="api"),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

print("\nNews fetching tasks get started here, It will run once and every subsequent five minutes.\n")
tasks.start()
