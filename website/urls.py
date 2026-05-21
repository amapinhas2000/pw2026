from django.urls import path
from .views import *

urlpatterns = [

    path('', Index.as_view(), name='inicio'),

    path('servico/', ServicoTemplateView.as_view(), name='servico'),

    path('contato/', Contato.as_view(), name='contato'),

    path('barbeiro/', Barbeiro.as_view(), name='barbeiro'),

    path('agendar/', AgendamentoCreate.as_view(), name='agendar'),

    path('listar/', AgendamentoList.as_view(), name='listar_agendamento'),

    path('detalhar/<int:pk>/',
         AgendamentoDetail.as_view(),
         name='detalhar_agendamento'),

    path('editar/<int:pk>/',
         AgendamentoUpdate.as_view(),
         name='editar_agendamento'),

    path('excluir/<int:pk>/',
         AgendamentoDelete.as_view(),
         name='excluir_agendamento'),
]