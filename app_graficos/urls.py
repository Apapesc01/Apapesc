from django.urls import path

from . import views

from .views import GraficosSuperView, DefesoChartsData

app_name = 'app_graficos'

urlpatterns = [
    path('super/', GraficosSuperView.as_view(), name='supergraficos'), 
    path('dados/defeso/', DefesoChartsData.as_view(), name="graficos_defeso_json"),
]
