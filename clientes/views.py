from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Cliente
from .models import Carro
import re
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

def clientes(request):
    if request.method == 'GET':
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes':clientes_list})

    elif request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf = cpf)
        

        if cliente.exists():
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'email':email, 'carros':zip(carros, placas, anos)})

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'cpf':cpf, 'carros':zip(carros, placas, anos)})

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        list_placas = Carro.objects.filter(placa=placa)
        
        if list_placas.exists():
            return HttpResponse('Palca ja existente')

        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro = carro, placa = placa, ano = ano, cliente = cliente)
            car.save()

        return HttpResponse('teste')

def att_clientes(request):
    id_cliente = request.POST.get('id_cliente')
    
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])
    
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': carro['fields', 'id':carro['pk']]} for carro in carros_json]
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    data = {'cliente':cliente_json, 'carros':carros_json, 'cliente_id':cliente_id}

    return JsonResponse(data)

@csrf_exempt
def update_carro(request, id):
    nome_carro = request.POST.get('carro')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')

    carro = Carro.objects.get(id=id)
    list_placas = Carro.objects.filter(placa=placa).exclude(id=id)
    if list_placas.exists():
        return HttpResponse('Placa ja existente')
    carro.carro = nome_carro
    carro.placa = placa
    carro.ano = ano
    carro.save()


def excluir_carro(request, id):
    try:
        carro = Carro.objects.get(id=id)
        carro.delete()
        return redirect(reverse('clientes')+f'?aba=att_clientes&id_cliente={id}')
    except:
        return redirect(reverse('clientes')+f'?aba=att_clientes&id_cliente={id}')

def update_cliente(request, id):
    corpo = json.loads(request.body)

    nome = corpo['nome']
    sobrenome = corpo['sobrenome']
    email = corpo['email']
    cpf = corpo['cpf']


    cliente = get_object_or_404(Cliente, id=id)

    try:
        cliente.nome = nome
        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf 
        cliente.save()

        return JsonResponse({'status':'200','nome':nome,'sobrenome':sobrenome,'email':email,'cpf':cpf})

    except:
        return JsonResponse({'status':'500'})   