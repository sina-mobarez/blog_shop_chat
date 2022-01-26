from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from accounts.views import LoginView, RegisterUser, RegisterView, VerifyView, ResendVerifyView, LoginUser
from . import settings
from shop.views import LandingPage
from chat.views import search




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
                  
                  path('auth/', include('djoser.urls')),
                  path('auth/', include('djoser.urls.jwt')),
                  path('otp/', include('accounts.urls')),
	
	              
                  path("api/v1/",include("webservice.urls")),
                  path('chat/', include('chat.urls')),
                  path('admin/', admin.site.urls),
                  path('login/', LoginView.as_view(), name='login'),
                  path('verify/', VerifyView.as_view(), name='verify'),
                  path('verify/resend/', ResendVerifyView.as_view(), name='resend'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('blog/', include('blog.urls')),
                  path('api/register', RegisterUser.as_view(), name='api-register'),
                  path('api/login', LoginUser.as_view(), name='api-login'),
                  path('chatroom/searched/', search, name='chat-search'),

                  path('accounts/', include('django.contrib.auth.urls')),
                  path('', LandingPage.as_view(), name='landing-page'),
                   
                  url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
