from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = (
    [   
        # Django Website
        path("", include("pages.urls")),
        path("listings/", include("listings.urls")),
        path("instructors/", include("instructors.urls")),
        path("accounts/", include("accounts.urls")),
        path("contacts/", include("contacts.urls")),
        # Django Admin
        path("admin/", admin.site.urls),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
