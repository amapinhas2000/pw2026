from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

    
class Horario(models.Model):
    inicio = models.TimeField()
    fim = models.TimeField()
    
    def __str__(self):
        return f"{self.inicio} às {self.fim}"

class Agendamento(models.Model):
    nome_cliente = models.CharField(max_length=100)
    servico = models.ForeignKey(Servico, on_delete=models.PROTECT)
    horario = models.ForeignKey(Horario, on_delete=models.PROTECT)
    data = models.DateField()

    def __str__(self):
        return self.nome_cliente
    
class Faturamento(models.Model):
    agendamento = models.ForeignKey(
        Agendamento,
        on_delete=models.CASCADE
    )

    valor = models.DecimalField(
    max_digits=6,
    decimal_places=2
    )
    
class Barbeiro(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)

    def __str__(self):
         return self.nome

class Feedback(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()
    comentario = models.TextField() 

    def __str__(self):
        return f"O cliente {self.cliente} deu uma nota de {self.nota} "