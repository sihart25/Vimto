"""vimto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework.authtoken.views import ObtainAuthToken

from vimto_ws import rest_api
from vimto import views
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.conf import settings


class ObtainAuthToken2(ObtainAuthToken):

    def get_serializer_class(self):
        return AuthTokenSerializer


url_rest_patterns = [
    url(r'^vimto/', rest_api.Vimto_wsView.as_view(), name='vimto_ws'),
    url(r'^rest-docs/', include('rest_framework_swagger.urls')),
    url(r'^auth-token/', ObtainAuthToken2.as_view()),
]

urlpatterns = [
    url(r'^accounts/', include('vimto_auth.urls', namespace="accounts")),
    url(r'^{}/admin/'.format(settings.ADMIN_URL_PATH), include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^polls/', include('polls.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.extend(url_rest_patterns)
