from django.urls import path

from . import views

from .views import GraficosSuperView

app_name = 'app_graficos'

urlpatterns = [
    path('super/', GraficosSuperView.as_view(), name='supergraficos'), 
]
