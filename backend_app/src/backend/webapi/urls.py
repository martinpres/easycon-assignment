"""
URL configuration for webapi project.

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
from django.urls import path

from backend.webapi.views import MQTTMetaDataView, ModbusDataView, ControlPublisherView, MQTTDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/data/mqtt/meta", MQTTMetaDataView.as_view(), name="api-data-mqtt-meta"),
    path("api/data/mqtt", MQTTDataView.as_view(), name="api-data-mqtt"),
    path("api/data/modbus", ModbusDataView.as_view(), name="api-data-modbus"),
    path("api/control/", ControlPublisherView.as_view(), name="api-control")
]
