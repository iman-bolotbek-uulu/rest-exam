"""exam URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view


from account import views as acc_views
from news import views as news_views

acc_router = routers.DefaultRouter()
acc_router.register('register', acc_views.AuthorRegisterViewSet)

news_router = routers.DefaultRouter()
news_router.register('news', news_views.NewsViewSet)
news_router.register('status', news_views.StatusViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="Exam",
      default_version='v1',
      description="Exam",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="iman@gmail.com"),
      license=openapi.License(name="No License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/auth/token/', obtain_auth_token),

    path('api/account/', include(acc_router.urls)),
    path('api/', include(news_router.urls)),
    path('api/news/<int:news_id>/comment/', news_views.CommentListCreateAPIView.as_view()),
    path('api/news/<int:news_id>/comment/<int:pk>/', news_views.CommentRetrieveUpdateAPIView.as_view()),

    path('api/news/<int:news_id>/<slug:slug>/', news_views.status_news),
    path('api/news/<int:news_id>/comment/<int:comment_id>/<slug:slug>/', news_views.status_comment),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger_doc'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc_doc'),
]
