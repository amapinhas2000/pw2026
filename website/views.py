from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
    ListView
)

from django.urls import reverse_lazy
from .models import Agendamento, Horario, Servico
from django.contrib import messages
from datetime import datetime, timedelta


class Index(TemplateView):
    template_name = "website/inicio.html"

class ServicoTemplateView(TemplateView):
    template_name = "website/servico.html"  

class Contato(TemplateView):
    template_name = "website/contato.html"

class Barbeiro(TemplateView):
    template_name = "website/barbeiro.html"

class VerAgendamentos(TemplateView):

    template_name = "website/ver_agendamentos.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['agendamentos'] = (
            Agendamento.objects.all().order_by('data')
        )

        return context


class AgendamentoCreate(CreateView):
    model = Agendamento
    fields = ['nome_cliente', 'servico', 'data']
    template_name = 'website/agendar.html'
    success_url = reverse_lazy('listar_agendamento')

    def form_valid(self, form):

        data_final = form.cleaned_data['data']

        if Agendamento.objects.filter(data=data_final).exists():
            form.add_error('data', 'Horário já ocupado ❌')
            return self.form_invalid(form)

        messages.success(self.request, "Agendado com sucesso ✅")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['horarios'] = Horario.objects.all()
        context['servicos'] = Servico.objects.all()
        return context

class AgendamentoUpdate(UpdateView):
    model = Agendamento
    fields = ['nome_ciente', 'servico', 'data']
    template_name = 'website/agendar.html'
    success_url = reverse_lazy('listar_agendamento')

class AgendamentoDelete(DeleteView):
    model = Agendamento
    template_name = 'website/excluir.html'
    success_url = reverse_lazy('listar_agendamento')

class AgendamentoDetail(DetailView):
    model = Agendamento
    template_name = 'website/detalhar.html'

class AgendamentoList(ListView):
    model = Agendamento
    template_name = 'website/listar.html'
    context_object_name = 'agendamentos'