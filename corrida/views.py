from django.shortcuts import render, redirect, get_object_or_404
from espumas.models import *
from .models import ElementoCorrida, Corrida, BloqueMedidas, BloqueProducido
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template.loader import get_template
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect

#from django.core.mail import EmailMessage


def _corrida_actual():
	try:
		corrida = Corrida.objects.get(pre_orden= True)
	except Corrida.DoesNotExist:
		corrida = Corrida.objects.create()
		corrida.save()
	return corrida

def agrega_a_corrida(request, bloque_medidas_id):
	bloqueMedidas = BloqueMedidas.objects.get(id=bloque_medidas_id)
	corrida = _corrida_actual()
	try:
		elemento_corrida = ElementoCorrida.objects.get(bloqueMedidas= bloqueMedidas, corrida=corrida)
		elemento_corrida.cantidad += 1
		elemento_corrida.save()
	except ElementoCorrida.DoesNotExist:
		elemento_corrida = ElementoCorrida.objects.create(
					bloqueMedidas = bloqueMedidas,
					corrida = corrida,
					cantidad = 1
			)
		elemento_corrida.save()
		# arreglar el redirect
	return redirect('espumas:espumas')


def orden_de_corrida(request):
	if request.method == 'POST':
		cantidades = request.POST.getlist('cantidades')
		ids = request.POST.getlist('elementoIds')
		fecha_programada = request.POST.get('fecha_programada')
		print(cantidades)
		print(ids)
		for index, cantidad in enumerate(cantidades):
			elementoCorrida = ElementoCorrida.objects.get(id=ids[index])
			elementoCorrida.cantidad = cantidad
			elementoCorrida.save()
			print("Save successful perro")
		corrida = _corrida_actual()
		corrida.fecha_programada = fecha_programada
		corrida.pre_orden = False
		corrida.pendiente_produccion = True
		corrida.save()
		#arreglar el redirect a catalogo de corridas
		#redirigir a las ordenes de corridas
	return redirect('corrida:ordenes_pendientes')


def remover_elemento_catalogo(request, elemento_id):
	elemento = ElementoCorrida.objects.get(pk= elemento_id)
	elemento.delete()
	return redirect('espumas:espumas')

def remover_elemento_ordenes(request, elemento_id):
	elemento = ElementoCorrida.objects.get(pk= elemento_id)
	elemento.delete()
	return redirect('corrida:ordenes')

def remover_elemento_ordenes_pendientes(request, elemento_id):
	elemento = ElementoCorrida.objects.get(pk= elemento_id)
	elemento.delete()
	return redirect('corrida:ordenes_pendientes')


#
# def ordenes(request):
# 	item_list = ElementoCorrida.objects.all()
# 	context ={
# 		'itemsFront':item_list,
# 	}
# 	return render(request,'corrida:ordenes/ordenes.html',context)
def ordenes(request):
	corridas = Corrida.objects.all()
	corridas_list =[]
	for corrida in corridas:
		elementos = ElementoCorrida.objects.filter(corrida = corrida)
		corridas_list.append(list(elementos))
	print(corridas_list)
	context ={
		'corridasFront': corridas_list,
		}
	return render(request,'ordenes/ordenes.html',context)

def ordenes_pendientes(request):
	corridas_pendientes = Corrida.objects.filter(pendiente_produccion= True)
	corridas_en_produccion = Corrida.objects.filter(en_produccion=True)
	corridas_pendientes_list = []
	corridas_en_produccion_list = []
	for corrida in corridas_pendientes:
		elementos = ElementoCorrida.objects.filter(corrida = corrida)
		corridas_pendientes_list.append(list(elementos))

	for corrida in corridas_en_produccion:
		elementos = ElementoCorrida.objects.filter(corrida = corrida)
		corridas_en_produccion_list.append(list(elementos))
	context ={
		'corridas_pendientes': corridas_pendientes_list,
		'corridas_en_produccion': corridas_en_produccion_list,
	}
	return render(request, 'ordenes/ordenes_pendientes.html', context)

def producir_corrida(request, corrida_id):
	try:
		corrida = Corrida.objects.get(pk= corrida_id)
		corrida.pendiente_produccion = False
		corrida.en_produccion = True
		corrida.save()
	except Corrida.DoesNotExist:
		#error corrida no existe
		pass
	return redirect('corrida:ordenes_pendientes')

def producir_bloques(request, corrida_id, elementoCorrida_id=None):
	elementos = ElementoCorrida.objects.filter(corrida = corrida_id)
	if elementoCorrida_id:
		elementoCorrida = ElementoCorrida.objects.get(id= elementoCorrida_id)
	else:
		elementoCorrida = elementos[0]
	bloqueMedidas = BloqueMedidas.objects.get(id = elementoCorrida.bloqueMedidas.id)
	bloquesProducidos = BloqueProducido.objects.filter(elemento_corrida= elementoCorrida.id)
	defectos = BloqueProducido.DEFECTOS_CHOICES
	context ={
        'elementoCorrida': elementoCorrida,
        'bloqueMedidas': bloqueMedidas,
        'elementos': elementos,
		'bloquesProducidos': bloquesProducidos,
		'tipos_defectos':defectos,
    }
	return render(request, 'ordenes/produccion.html',context) 



def producir_bloque_seleccionado (request):
	if request.method == 'POST':
		print(request.POST)
		print(request.POST.get('revision_calidad'))
		elemento_corrida = ElementoCorrida.objects.get(id=request.POST.get('elemento_corrida'))

		bloque_producido = BloqueProducido()

		bloque_producido.no_de_bloque = 1
		bloque_producido.elemento_corrida_id = request.POST.get('elemento_corrida')
		bloque_producido.revision_calidad = request.POST.get('revision_calidad')
		bloque_producido.defecto = request.POST.get('defecto')
		bloque_producido.alto_caliente = request.POST.get('alto_caliente')
		bloque_producido.peso_caliente = request.POST.get('peso_caliente')
		bloque_producido.flujo_de_aire_caliente = request.POST.get('flujo_de_aire_caliente')
		bloque_producido.save()

	return redirect( 'corrida:producir_bloques', ) 
		


def cancelar_corrida(request, corrida_id):
	try:
		corrida = Corrida.objects.get(pk= corrida_id)
		corrida.pendiente_produccion = False
		corrida.en_produccion = False
		corrida.pre_orden = False
		corrida.cancelada = True
		corrida.save()
	except Corrida.DoesNotExist:
		#error corrida no existe
		pass
	return redirect('corrida:ordenes_pendientes')
	
def editar_cantidades_corrida(request):
	if request.method == 'POST':
		cantidades = request.POST.getlist('cantidades')
		ids = request.POST.getlist('elementoIds')
		print(cantidades)
		print(ids)
		for index, cantidad in enumerate(cantidades):
			elementoCorrida = ElementoCorrida.objects.get(id=ids[index])
			elementoCorrida.cantidad = cantidad
			elementoCorrida.save()
			print("Save successful perro")
		return redirect('corrida:ordenes_pendientes')
