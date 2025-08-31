"""
URL configuration for autograder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
    openapi.Info(
        title="Autograder API",
        default_version="v1",
        description="API documentation for the Autograder backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    [
        # API documentation
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("djangoadmin/", admin.site.urls),
    # Modern DRF API endpoints
    path("api/", include("autograder.api.urls")),
        path("", include("autograder.apps.index.urls", namespace="index")),
        path("oauth/", include("autograder.apps.oauth.urls", namespace="oauth")),
        path(
            "contests/", include("autograder.apps.contests.urls", namespace="contests")
        ),
        path(
            "problems/", include("autograder.apps.problems.urls", namespace="problems")
        ),
        path("status/", include("autograder.apps.runtests.urls", namespace="runtests")),
        path(
            "rankings/", include("autograder.apps.rankings.urls", namespace="rankings")
        ),
        path("tjioi/", include("autograder.apps.tjioi.urls", namespace="tjioi")),
        path("", include("social_django.urls", namespace="social")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
