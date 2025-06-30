from django.urls import path


from .views import (
    SuperDashboardView
    )


app_name = 'app_dashboards'

urlpatterns = [
    path('SuperDash/', SuperDashboardView.as_view(), name='super_dashboard'), # Super Usuários
    
]