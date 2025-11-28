"""
URL configuration for zzApp_core project.

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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('adm-samcris-2022/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('account/', include('app_accounts.urls', namespace="app_accounts")),    
    path('', include('app_home.urls', namespace="app_home")),
    path('associacao/', include('app_associacao.urls', namespace="app_associacao")),
    path('associados/', include('app_associados.urls', namespace="app_associados")),
    path('uploads/', include('app_uploads.urls', namespace='app_uploads')),
    path('anuidades/', include('app_anuidades.urls', namespace='app_anuidades')),
    path('dashboards/', include('app_dashboards.urls', namespace='app_dashboards')),
    path('inss', include('app_inss.urls', namespace='app_inss')),
    path('seguro-defeso/', include('app_defeso.urls', namespace='app_defeso')),
    path('reap/', include('app_reap.urls', namespace='app_reap')),
    path('servicos/', include('app_servicos.urls', namespace='app_servicos')),
    path('automacoes/', include('app_automacoes.urls', namespace='app_automacoes')),
    path('embarcacoes/', include('app_embarcacoes.urls', namespace='app_embarcacoes')),
    path('despesas/', include('app_despesas.urls', namespace='app_despesas')),
    path('graficos/', include('app_graficos.urls', namespace='app_graficos')),


    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)