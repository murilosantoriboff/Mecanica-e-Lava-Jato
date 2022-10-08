from django.db.models import TextChoices

class ChoicesCategoriasManuntencao(TextChoices):
    TROCAR_VALVULA_MOTOR = 'TVM', 'Trocar valvula do motor'
    TROCAR_OLEO = 'TO', 'Trocar oleo do motor'
    BALENCEAMENTO = 'b', 'Balenceamento'