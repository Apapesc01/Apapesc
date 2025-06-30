from django.urls import path


from .views import (
    CreateAnuidadeView,
    LancamentosAnuiadesListView,
    AnuidadeAssociadoSingleView
    )


app_name = 'app_anuidades'

urlpatterns = [
    path('create/', CreateAnuidadeView.as_view(), name='create_anuidade'),
    path('lançamentos-anuidades/', LancamentosAnuiadesListView.as_view(), name='list_anuidades'),
    path('anuidade-assocado/<int:pk>/', AnuidadeAssociadoSingleView.as_view(), name='anuidade_associado_singular')
]