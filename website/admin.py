from django.contrib import admin
from .models import (
    PerfilUsuario, Servico, Barbeiro, Cliente,
    HorarioDisponivel, Agendamento, MensagemContato,
    Feedback, FotoTrabalho
)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo_usuario", "telefone", "criado_em")
    list_filter = ("tipo_usuario",)
    search_fields = ("usuario__username", "telefone")

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "preco", "duracao_minutos", "ativo", "destaque", "ordem")
    list_filter = ("ativo", "destaque", "categoria")
    search_fields = ("nome", "descricao")

@admin.register(Barbeiro)
class BarbeiroAdmin(admin.ModelAdmin):
    list_display = ("nome", "cargo", "especialidade", "ativo")
    list_filter = ("ativo",)
    search_fields = ("nome", "cargo", "especialidade")

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone", "email", "cadastrado_em")
    search_fields = ("nome", "telefone", "email")

@admin.register(HorarioDisponivel)
class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ("barbeiro", "horario", "ativo", "observacao")
    list_filter = ("ativo", "barbeiro")

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "servico", "barbeiro", "data", "horario", "status")
    list_filter = ("status", "data", "barbeiro")
    search_fields = ("cliente__nome", "servico__nome")

@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone", "lida", "enviada_em")
    list_filter = ("lida", "enviada_em")
    search_fields = ("nome", "email", "mensagem")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("cliente", "barbeiro", "nota", "criado_em", "aprovado")
    list_filter = ("nota", "aprovado")
    search_fields = ("cliente__nome", "comentario")

@admin.register(FotoTrabalho)
class FotoTrabalhoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "barbeiro", "categoria", "publicado", "criado_em")
    list_filter = ("categoria", "publicado", "barbeiro")
    search_fields = ("titulo", "descricao")