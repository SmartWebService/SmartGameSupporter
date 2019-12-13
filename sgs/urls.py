"""sgs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
import core.views
import game.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core.views.lobby, name='lobby'),
    path('new', core.views.new, name='new'),
    path('join', core.views.join, name='join'),
    path('room/<int:game_code>', core.views.room, name='room'),
    path('game/<int:game_code>', game.views.in_game, name='game'),
    path('api/iot/<int:device_code>', core.views.api_iot, name='iot'),
    url(r'^sgs/', include('core.urls')),
]
