from secrets import token_hex
from django.db import models
from clientes.models import Cliente
from .choices import ChoicesCategoriasManuntencao
from datetime import datetime

class CategoriasManutenção(models.Model):
    titulo = models.CharField(max_length=3, choices = ChoicesCategoriasManuntencao.choices)
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.titulo

class Servico(models.Model):
    titulo = models.CharField(max_length=30)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    categoria_manuntecao = models.ManyToManyField(CategoriasManutenção)
    data_inicio = models.DateField(null=True)
    data_entrega = models.DateField(null=True)
    finalizado = models.BooleanField(default=False)
    protocolo = models.CharField(max_length=52, null=True, blank = True)

    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = datetime.now().strftime("%d/%m/%Y - %H:%M:%S - ") + token_hex(16)
        super(Servico, self).save(*args, **kwargs)

    def preco_total(self):
        preco_total = float(0)
        for categoria in self.categoria_manuntecao.all():
            preco_total += float(categoria.preco)

        return preco_total