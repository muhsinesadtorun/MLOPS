from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.views.static import serve
from home.views import home_view
#from django.conf.urls.static import static
#from django.conf import settings


urlpatterns = [

    path( '', home_view, name='home'),

    path("post/", include("post.urls")),

    path("admin/", admin.site.urls),

]

urlpatterns += [
        path(
            "media/<path>",
            serve,
            {
                "document_root": settings.MEDIA_ROOT,
            },
        ),
    ]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)