from django.contrib import admin

from .models import (
    Servico,
    Horario,
    Agendamento,
    Faturamento,
    Barbeiro,
    Cliente,
    Feedback
)

admin.site.register(Servico)
admin.site.register(Horario)
admin.site.register(Agendamento)
admin.site.register(Faturamento)
admin.site.register(Barbeiro)
admin.site.register(Cliente)
admin.site.register(Feedback)