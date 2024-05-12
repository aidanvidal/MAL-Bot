"""
URL configuration for MAL_app project.

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

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("MAL_app.urls")),
    path("login/", include("MAL_app.urls")),
    path("home/", include("MAL_app.urls")),
    path("token/", include("MAL_app.urls")),
    path("create/", include("MAL_app.urls")),
    path("process_input/", include("MAL_app.urls")),
    path("logout/", include("MAL_app.urls")),
    path("generate_token_link/", include("MAL_app.urls")),
]
