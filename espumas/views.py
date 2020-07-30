from django.shortcuts import render
#from .forms import *

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
#from .forms import SignUpForm
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.template.loader import get_template
from django.template import loader
#from .models import Cantidadp
from corrida.models import Corrida, ElementoCorrida
from django.db.models import Count
from .forms import *



def index(request):
    return render(request, 'index.html')

# def espumas(request):
#     return HttpResponse('espumas Respuesta http: Hola')

def respuesta(request):
    return HttpResponse('Respuesta http: Hola')

#funcion para la corrida actual
#esta func entrega la activa=true y si no existe la crea
def _corrida_actual():
    try:
        corrida = Corrida.objects.get(pre_orden= True)
    except Corrida.DoesNotExist:
        corrida = Corrida.objects.create()
        corrida.save()
    return corrida

def espumas(request, tipo_id=0):
    if tipo_id != 0:
        bloques_medidas = BloqueMedidas.objects.filter(tipo_de_espuma=tipo_id)
    else:
        bloques_medidas = BloqueMedidas.objects.filter(tipo_de_unidad__tipo_de_unidad ="Normal").filter(disponible = True)
    corrida = _corrida_actual()
    formas= Formas.objects.all()

    try:
        elementos_corrida = ElementoCorrida.objects.filter(corrida = corrida)
    except ElementoCorrida.DoesNotExist:
        elementos_corrida = None
    context ={
        'bloques_medidas':bloques_medidas,
        'elementos_corrida': elementos_corrida,
        'formas':formas,
        'tipo_id':tipo_id,
    }
    return render(request,'espumas/espumas.html',context)



#----MEDIDAS----


def medidas(request,tipo_id=0):
    if tipo_id !=0:
        item_list = BloqueMedidas.objects.filter(tipo_de_espuma=tipo_id)
    else:
        item_list = BloqueMedidas.objects.all()
    tde_menus= Tipos_de_Espuma.objects.all()
    context ={
        'itemsFront':item_list,
        'menufront':tde_menus,
    }
    return render(request,'espumas/medidas/medidas.html',context)

def detalle_medidas(request,item_id):
    item = BloqueMedidas.objects.get(pk=item_id)
    context = {
        'itemsFront':item,
        # 'header':'blocks'
    }
    return render(request,'espumas/medidas/detallemedidas.html',context)


def agregar_medidas(request):
    form = medidasForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('espumas:medidas')

    return render(request,'espumas/medidas/agregarmedidas.html',{'form':form})


def editar_medidas(request,id):
    item = BloqueMedidas.objects.get(id=id)
    form =medidasForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('espumas:medidas')

    return render(request,'espumas/medidas/agregarmedidas.html',{'form':form,'item':item})


def borrar_medidas(request,id):
    item = BloqueMedidas.objects.get(id=id)

    if request.method =='POST':
        item.delete()
        return redirect('espumas:medidas')
    return render(request,'espumas/medidas/borrarmedidas.html',{'item':item})



#-----TIPO DE Espuma-----

def tde(request):
    item_list = Tipos_de_Espuma.objects.all()
    context ={
        'itemsFront':item_list,
    }
    return render(request,'espumas/tde/tde.html',context)

def detalle_tde(request,item_id):
    item = Tipos_de_Espuma.objects.get(pk=item_id)
    context = {
        'itemsFront':item,
        # 'header':'blocks'
    }
    return render(request,'espumas/tde/detalletde.html',context)


def agregar_tde(request):
    form = tdeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('espumas:tde')

    return render(request,'espumas/tde/agregartde.html',{'form':form})


def editar_tde(request,id):
    item = Tipos_de_Espuma.objects.get(id=id)
    form =tdeForm(request.POST or None, instance=item)

    if form.is_valid():
        form.save()
        return redirect('espumas:tde')

    return render(request,'espumas/tde/agregartde.html',{'form':form,'item':item})


def borrar_tde(request,id):
    item = Tipos_de_Espuma.objects.get(id=id)

    if request.method =='POST':
        item.delete()
        return redirect('espumas:tde')
    return render(request,'espumas/tde/borrartde.html',{'item':item})



def formas(request):
    item_list = Formas.objects.all()
    context ={
        'itemsFront':item_list,
    }
    return render(request,'espumas/selectores/formas.html',context)