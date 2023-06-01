from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.views.static import serve
from home.views import home_view
#from django.conf.urls.static import static
#from django.conf import settings
from prometheus_client import exposition
from post.metrics import REGISTRY
from django_prometheus import exports

urlpatterns = [

    path( '', home_view, name='home'),
    
    #path('', include('django_prometheus.urls')),

    path('metrics/', exports.ExportToDjangoView, name='metrics'),

    path("post/", include("post.urls")),
    
    path("accounts/", include("accounts.urls")),

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
        path(
            "static/<path>",
            serve,
            {
                "document_root": settings.STATIC_ROOT,
            },
        ),
    ]
