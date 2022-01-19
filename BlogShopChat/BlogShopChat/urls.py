"""BlogShopChat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from accounts.views import LoginView, RegisterUser, RegisterView, login_user
from . import settings
from shop.views import LandingPage




schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
                  path('grappelli/', include('grappelli.urls')),
                  path('shop/', include('shop.urls')),
                  #path to djoser end points
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.jwt')),
	
	              #path to our account's app endpoints
                  path("api/v1/",include("webservice.urls")),
                  path('chat/', include('chat.urls')),
                  path('admin/', admin.site.urls),
                  path('login/', LoginView.as_view(), name='login'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('blog/', include('blog.urls')),
                  path('api/register', RegisterUser.as_view(), name='api-register'),
                  path('api/login', login_user, name='api-login'),

                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', LandingPage.as_view(), name='landing-page'),
                  # swagger 
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
