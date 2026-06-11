from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class PerfilUsuario(models.Model):
    TIPO_CHOICES = [
        ("cliente", "Cliente"),
        ("barbeiro", "Barbeiro"),
        ("administrador", "Administrador"),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES, default="cliente")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    foto_perfil = models.ImageField(upload_to="perfis/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_usuario_display()}"


class Servico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    duracao_minutos = models.PositiveIntegerField()
    categoria = models.CharField(max_length=50, blank=True, null=True)
    icone = models.CharField(max_length=50, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    ordem = models.IntegerField(default=0)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Barbeiro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=200)
    descricao_curta = models.TextField()
    imagem_url = models.CharField(max_length=255, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    observacoes = models.TextField(blank=True, null=True)
    cadastrado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.telefone})"


class HorarioDisponivel(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, related_name="horarios_disponiveis")
    horario = models.TimeField()
    ativo = models.BooleanField(default=True)
    observacao = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ("barbeiro", "horario")
        verbose_name = "Horário Disponível"
        verbose_name_plural = "Horários Disponíveis"

    def __str__(self):
        return f"{self.barbeiro.nome} - {self.horario.strftime('%H:%M')}"


class Agendamento(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("confirmado", "Confirmado"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado"),
    ]
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name="agendamentos")
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT, related_name="agendamentos")
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.PROTECT, related_name="agendamentos")
    data = models.DateField()
    horario = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["barbeiro", "data", "horario"],
                condition=~models.Q(status="cancelado"),
                name="unique_agendamento_ativo_por_horario"
            )
        ]

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.nome} com {self.barbeiro.nome} em {self.data} às {self.horario}"


class MensagemContato(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    enviada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.nome} - {self.email}"


class Feedback(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="feedbacks")
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, related_name="feedbacks")
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, related_name="feedbacks")
    nota = models.IntegerField()
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    aprovado = models.BooleanField(default=True)

    def __str__(self):
        return f"Nota {self.nota} para {self.barbeiro.nome} por {self.cliente.nome}"


class FotoTrabalho(models.Model):
    CATEGORIA_CHOICES = [
        ("corte", "Corte"),
        ("barba", "Barba"),
        ("corte_barba", "Corte + Barba"),
        ("infantil", "Infantil"),
        ("outro", "Outro"),
    ]
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE, related_name="fotos_trabalho")
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to="trabalhos/")
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default="corte")
    publicado = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo