"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as autViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('center',include('center.urls',namespace='center')),
    path('vaccine',include('vaccin.urls',namespace='vaccin')),
    path('accounts/',include('user.urls',namespace='user')),
    path("password_reset/", autViews.PasswordResetView.as_view(), name="password_reset"),
    path("campaign/", include('campaign.urls',namespace='campaign')),
    path('vaccination/',include('vaccination.urls',namespace='vaccination')),
    path(
        "password_reset/done/",
        autViews.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        autViews.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        autViews.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),

]


urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Book My Vaccine'
admin.site.site_title = 'Book My Vaccine'
admin.site.index_title = 'Admin Panel'
