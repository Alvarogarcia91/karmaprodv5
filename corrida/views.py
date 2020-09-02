from django.shortcuts import render, redirect, get_object_or_404
from espumas.models import *
from .models import ElementoCorrida, Corrida, BloqueMedidas, BloqueProducido, Lote
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template.loader import get_template
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Max, Count, Sum, Avg
from datetime import datetime

#from django.core.mail import EmailMessage


#funcion para la corrida actual
#esta func entrega la activa=true y si no existe la crea
def _corrida_actual():
	try:
		corrida = Corrida.objects.get(pre_orden= True)
	except Corrida.DoesNotExist:
		corrida = Corrida.objects.create()
		corrida.save()
	return corrida

def nueva_corrida(request, forma_id=1, tipo_de_espuma_id=0):
    if tipo_de_espuma_id:
        bloques_medidas = BloqueMedidas.objects.filter(tipo_de_espuma_id = tipo_de_espuma_id).filter(forma_id = forma_id).filter(tipo_de_unidad__tipo_de_unidad ="Normal").filter(disponible = True)
    else:
        bloques_medidas = BloqueMedidas.objects.filter(forma_id = forma_id).filter(tipo_de_unidad__tipo_de_unidad ="Normal").filter(disponible = True)

    corrida = _corrida_actual()
    tipos_de_espuma = Tipos_de_Espuma.objects.all()

    conflicto = False
    try:
        elementos_corrida = ElementoCorrida.objects.filter(corrida = corrida)
        if elementos_corrida[0].bloqueMedidas.forma_id != forma_id:
            conflicto = True
    except IndexError:
        elementos_corrida = None
    context ={
        'conflicto' : conflicto,
        'bloques_medidas':bloques_medidas,
        'elementos_corrida': elementos_corrida,
        'tipos_de_espuma':tipos_de_espuma,
        'forma_id':forma_id,
    }
    return render(request,'espumas/espumas.html',context)


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
		
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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

def remover_elemento_corrida(request, elemento_id):
	elemento = ElementoCorrida.objects.get(pk = elemento_id)
	elemento.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

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
	corridas_pendientes = Corrida.objects.filter(pendiente_produccion= True).prefetch_related('elementocorrida_set__bloqueMedidas__tipo_de_espuma').prefetch_related('elementocorrida_set__bloqueMedidas__tipo_de_unidad').prefetch_related('elementocorrida_set__bloqueMedidas__forma')
	context ={
		'corridas_pendientes': corridas_pendientes,
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
	return redirect('corrida:producir_bloques',corrida_id )

def producir_bloques(request, corrida_id, elementoCorrida_id=None):
	elementos = ElementoCorrida.objects.filter(corrida = corrida_id).annotate(num_bloques = Count('bloqueproducido'))
	elementos_normales = elementos.filter(bloqueMedidas__tipo_de_unidad__tipo_de_unidad="Normal")
	opciones = None

	bloquesProducidos = BloqueProducido.objects.filter(elemento_corrida__corrida_id = elementos[0].corrida_id).order_by('-no_de_bloque')
	bloquesProducidosCount = bloquesProducidos.count()

	if elementoCorrida_id:
		elementoCorrida = ElementoCorrida.objects.get(id = elementoCorrida_id)
	else:	
		if bloquesProducidosCount:
			elementoCorrida = bloquesProducidos[0].elemento_corrida
		else:
			elementoCorrida = elementos[0]
	
	opciones = elementos.filter(bloqueMedidas__tipo_de_unidad__tipo_de_unidad = 'Normal')
	
	primer_bloque = True
	if bloquesProducidosCount:
		primer_bloque = False
	
	multiples_elementos = False
	if elementos_normales.count() > 1:
		multiples_elementos = True
	
	cilindro = False
	if elementos[0].bloqueMedidas.forma.forma == 'Cilindro':
		cilindro = True

	defectos = BloqueProducido.DEFECTOS_CHOICES
	
	context ={
		'elementoCorrida': elementoCorrida,
		'elementos': elementos,
		'bloquesProducidos': bloquesProducidos,
		'tipos_defectos':defectos,
		'opciones':opciones,
		'bloquesProducidosCount':bloquesProducidosCount,
		'primer_bloque': primer_bloque,
		'multiples_elementos': multiples_elementos,
		'cilindro': cilindro,
	}
	
	return render(request, 'ordenes/produccion.html',context) 

def monitoreo_de_produccion(request, corrida_id):
	
	elementos_corrida = ElementoCorrida.objects.filter(corrida = corrida_id).annotate(num_bloques = Count('bloqueproducido'))
	
	bloques_producidos = BloqueProducido.objects.filter(elemento_corrida__corrida_id = elementos_corrida[0].corrida_id).order_by('-no_de_bloque')
	bloques_producidos_count = bloques_producidos.count()
	bloques_rechazados_count = bloques_producidos.filter(revision_calidad = False).count()
	if bloques_producidos_count:
		bloques_aprobados_porcentaje = (bloques_producidos_count - bloques_rechazados_count)*100/bloques_producidos_count
	else:
		bloques_aprobados_porcentaje = 100
	
	context ={
		'elementos_corrida': elementos_corrida,
		'bloques_producidos': bloques_producidos,
		'bloques_producidos_count':bloques_producidos_count,
		'bloques_rechazados_count':bloques_rechazados_count,
		'bloques_aprobados_porcentaje': bloques_aprobados_porcentaje,
	}
	
	return render(request, 'ordenes/monitoreo.html', context)


def producir_bloque_seleccionado (request):
	if request.method == 'POST':
		elemento_corrida = ElementoCorrida.objects.get(id=request.POST.get('elemento_corrida'))
		elemento_siguiente = elemento_corrida
		bloque_medidas = elemento_corrida.bloqueMedidas
		
		if 'inicio' in request.POST:
			elemento_corrida_normal = ElementoCorrida.objects.get(id=request.POST.get('selectorInicio'))
			bloque_medidas = elemento_corrida_normal.bloqueMedidas
			bloque_medidas = BloqueMedidas.objects.filter(tipo_de_unidad__tipo_de_unidad ="Inicio").filter(familia_de_medidas = bloque_medidas.familia_de_medidas)[0]
			elemento_corrida_inicio = ElementoCorrida.objects.create(
					bloqueMedidas = bloque_medidas,
					corrida = elemento_corrida.corrida,
					cantidad = 1
			)
			elemento_corrida_inicio.save()
			elemento_corrida = elemento_corrida_inicio
			elemento_siguiente = elemento_corrida_normal

		if 'opcion' in request.POST:
			bloque_medidas = BloqueMedidas.objects.filter(tipo_de_unidad__tipo_de_unidad ="Cambio").filter(familia_de_medidas = bloque_medidas.familia_de_medidas)[0]
			elemento_corrida_cambio = ElementoCorrida.objects.create(
					bloqueMedidas = bloque_medidas,
					corrida = elemento_corrida.corrida,
					cantidad = 1
			)
			elemento_corrida_cambio.save()
			elemento_corrida = elemento_corrida_cambio
			elemento_siguiente = ElementoCorrida.objects.get(id=request.POST.get('selector'))

		bloque_producido = BloqueProducido()
		bloque_producido.elemento_corrida_id = elemento_corrida.id
		bloque_producido.revision_calidad = request.POST.get('revision_calidad') or False
		bloque_producido.defecto = request.POST.get('defecto')
		bloque_producido.peso_caliente = request.POST.get('peso_caliente')
		if bloque_medidas.forma != "Cilindro":
			bloque_producido.alto_caliente = request.POST.get('alto_caliente')
		bloque_producido.largo_caliente = request.POST.get('largo_caliente')
		bloque_producido.ancho_caliente = request.POST.get('ancho_caliente')
		bloque_producido.flujo_de_aire_caliente = request.POST.get('flujo_de_aire_caliente')
		bloque_producido.comentario = request.POST.get('comentario')
		
		if 'final' in request.POST:
			bloque_medidas = BloqueMedidas.objects.filter(tipo_de_unidad__tipo_de_unidad ="Final").filter(familia_de_medidas = bloque_medidas.familia_de_medidas)[0]
			elemento_corrida_final = ElementoCorrida.objects.create(
					bloqueMedidas = bloque_medidas,
					corrida = elemento_corrida.corrida,
					cantidad = 1
			)
			elemento_corrida_final.save()
			bloque_producido.elemento_corrida_id = elemento_corrida_final.id
			bloque_producido.save()

			corrida = Corrida.objects.get(pk=elemento_corrida.corrida_id )
			corrida.pendiente_produccion = False
			corrida.en_produccion = False
			corrida.pre_orden = False
			corrida.cancelada = False
			corrida.producto_terminado = True
			corrida.fecha_produccion = datetime.now()
			corrida.save()
			return redirect('corrida:corrida_producida',corrida)
		
		bloque_producido.save()


	return redirect( 'corrida:producir_bloques', corrida_id=elemento_corrida.corrida_id , elementoCorrida_id=elemento_siguiente.id  ) 
		


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
		# redirect al "resumen"
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


def corrida_producida(request,corrida_id):
	bloques_producidos = BloqueProducido.objects.filter(elemento_corrida__corrida_id = corrida_id).order_by('no_de_bloque')
	resumen = {
		"bloques_totales": 0,
		"bloques_normales": 0,
		"bloques_ok": 0,
		"bloques_ng": 0,
		"bloques_cambio": 0,
		"densidad_promedio": 0,
		"metros_planeados": 0,
		"metros_producidos": 0,
		"peso_producido": 0,
	}
	resumen['bloques_totales'] = bloques_producidos.count()
	resumen['bloques_normales'] = bloques_producidos.filter(elemento_corrida__bloqueMedidas__tipo_de_unidad__tipo_de_unidad = "Normal").count()
	resumen['bloques_ok'] = bloques_producidos.filter(revision_calidad = True).count()
	resumen['bloques_ng'] = bloques_producidos.filter(revision_calidad = False).count()
	resumen['bloques_cambio'] = bloques_producidos.filter(elemento_corrida__bloqueMedidas__tipo_de_unidad__tipo_de_unidad = "Cambio").count()
	resumen['metros_planeados'] = str(bloques_producidos.aggregate(Sum('elemento_corrida__bloqueMedidas__largo_frio_objetivo'))['elemento_corrida__bloqueMedidas__largo_frio_objetivo__sum']/100)
	resumen['metros_producidos'] = str(bloques_producidos.aggregate(Sum('largo_caliente'))['largo_caliente__sum']/100)
	resumen['densidad_promedio'] = bloques_producidos.aggregate(Avg('densidad'))['densidad__avg']
	resumen['peso_producido'] = str(bloques_producidos.aggregate(Sum('peso_caliente'))['peso_caliente__sum'])
	corrida = Corrida.objects.get(id=corrida_id)
	elementos_corrida = ElementoCorrida.objects.filter(corrida_id = corrida_id).filter(bloqueMedidas__tipo_de_unidad__tipo_de_unidad = "Normal")
	resumenes_por_tde = []
	for elemento in elementos_corrida:
		bloques = elemento.bloqueproducido_set.all()
		bloques_count = bloques.count()
		if bloques_count:
			ok_count = bloques.filter(revision_calidad = True).count()
			bloques_ng = bloques.filter(revision_calidad = False)
			ng_count = bloques_ng.count()
			porcentaje_ng = (ng_count/bloques_count)*100
			densidad_promedio = bloques.aggregate(Avg('densidad'))['densidad__avg']
			metros_planeados = str(bloques.aggregate(Sum('elemento_corrida__bloqueMedidas__largo_frio_objetivo'))['elemento_corrida__bloqueMedidas__largo_frio_objetivo__sum']/100)
			metros_producidos = str(bloques.aggregate(Sum('largo_caliente'))['largo_caliente__sum']/100)
			metros_ng = str(bloques_ng.aggregate(Sum('largo_caliente'))['largo_caliente__sum'] or 0)
			peso_producido = str(bloques.aggregate(Sum('peso_caliente'))['peso_caliente__sum'])
			
			resumen_tde ={
				"tde": elemento.bloqueMedidas.tipo_de_espuma.tipo_de_espuma,
				"normales_count": bloques_count,
				"ok_count": ok_count,
				"ng_count" : ng_count,
				"porcentaje_ng": porcentaje_ng,
				"densidad_promedio": densidad_promedio,
				"metros_planeados": metros_planeados,
				"metros_producidos": metros_producidos,
				"metros_ng": metros_ng,
				"peso_produdido": peso_producido,
				"area_de_curado": elemento.area_de_curado()
			}
			resumenes_por_tde.append(resumen_tde)

	context ={
		'bloques_producidos': bloques_producidos,
		'resumen': resumen,
		'resumenes_por_tde': resumenes_por_tde,
		'corrida': corrida,
	}
	return render(request ,'ordenes/corrida_producida.html' ,context )

def corridas_producidas(request):
	corridas_producidas = Corrida.objects.filter(producto_terminado= True).order_by('created')
	context ={
		'corridas_producidas': corridas_producidas

	}
	return render(request ,'ordenes/corridas_producidas.html' ,context )


def inventario(request):
	bloques_disponibles_sin_defecto = BloqueProducido.objects.filter( revision_calidad = True)
	bloques_disponibles_con_defecto = BloqueProducido.objects.filter( revision_calidad = False)
	tipos_de_espuma = Tipos_de_Espuma.objects.all()
	tipos_con_medidas = list()
	for  i, tipo_de_espuma in enumerate(tipos_de_espuma):
		medidas = BloqueMedidas.objects.filter(tipo_de_espuma = tipo_de_espuma).filter(tipo_de_unidad__tipo_de_unidad = 'Normal')
		tipos_con_medidas.append( { 'tipo_de_espuma':tipo_de_espuma,'medidas_con_count':list() } )
		for medida in medidas:
			bloques_producidos_count = BloqueProducido.objects.filter(elemento_corrida__bloqueMedidas = medida).count()
			tipos_con_medidas[i]['medidas_con_count'].append({'medida':medida,'bloques_producidos_count':bloques_producidos_count})
	print(tipos_con_medidas)
	




	# bloques_disponibles_sin_defecto = BloqueProducido.objects.filter( no_de_bloque = '4')


	# bloques_disponibles = BloqueProducido.objects.all()

	# normal_id = Tipos_de_Unidad.objects.filter(tipo_de_unidad='Normal')[0].id
	# bloques_disponibles = BloqueProducido.objects.filter( elemento_corrida__bloqueMedidas_tipo_de_unidad = normal_id)[0]

	# este me da los que no tienen defecto
	# bloques_disponibles = BloqueProducido.objects.filter( revision_calidad = True)

	#  este me da los tipos de unidad = normal
	# bloques_disponibles = BloqueProducido.objects.filter( elemento_corrida__bloqueMedidas__tipo_de_unidad__tipo_de_unidad = 'Normal')

	#  este filtra los alto calientes setting 116
	# bloques_disponibles = BloqueProducido.objects.filter( elemento_corrida__bloqueMedidas__alto_caliente_setting_predefinido = '116')

	# este filtra la cantidad =20
	# bloques_disponibles = BloqueProducido.objects.filter( elemento_corrida__cantidad = '20')


	# si funciona, filtra los no de blocque
	# bloques_disponibles = BloqueProducido.objects.filter( no_de_bloque = '4')

	# bloques_disponibles = BloqueProducido.objects.filter(elemento_corrida__corrida___producto_terminado = True)
	
	# num_bloques = 
	# result = Block.objects.filter(tipo_espuma='24-30').count()
	print(bloques_disponibles_sin_defecto)
	context ={
		'bloques_disponibles_sin_defecto': bloques_disponibles_sin_defecto,
		'bloques_disponibles_con_defecto':bloques_disponibles_con_defecto,
		'tipos_con_medidas':tipos_con_medidas,

	}
	return render(request ,'ordenes/inventario.html' ,context )

def dashboard_en_producion(request):
	corridas_en_produccion = Corrida.objects.filter(en_produccion = True).prefetch_related('elementocorrida_set__bloqueMedidas__tipo_de_espuma').prefetch_related('elementocorrida_set__bloqueMedidas__tipo_de_unidad')
	context ={
		'corridas_en_produccion': corridas_en_produccion,
	}
	return render(request,'ordenes/dashboard_en_producion.html',context)

def lotes(request):
	lotes_pendientes = Lote.objects.filter(pruebas_realizadas = False)
	lotes_aprobados = Lote.objects.filter(pruebas_pasadas = True)
	lotes_rechazados = Lote.objects.filter(pruebas_pasadas = False).filter(pruebas_realizadas = True)
	context = {
		'lotes_pendientes': lotes_pendientes,
		'lotes_aprobados': lotes_aprobados,
		'lotes_rechazados': lotes_rechazados,
	}
	return render(request,'ordenes/lotes.html', context)

def aprobar_lote(request, lote_id):
	lote = Lote.objects.get(id=lote_id)
	lote.dureza_capturada = request.POST.get('dureza_capturada')
	lote.sag_factor_capturado = request.POST.get('sag_factor_capturado')
	lote.densidad_capturada = request.POST.get('densidad_capturada')
	lote.flujo_de_aire_astm_capturado = request.POST.get('flujo_de_aire_astm_capturado')
	lote.pruebas_pasadas = request.POST.get('pruebas_pasadas')
	if 	request.POST.get('pruebas_pasadas'):
		lote.pruebas_pasadas = True
	else:
		lote.pruebas_pasadas = False
	if lote.dureza_capturada and lote.sag_factor_capturado and lote.densidad_capturada and lote.flujo_de_aire_astm_capturado:
		lote.pruebas_realizadas = True
	lote.save()
	return redirect('corrida:lotes')

def bloques_disponibles(request):
	#bloques_aprobados.filter(elemento_corrida__lote__pruebas_pasadas = True)
	bloques_disponibles = BloqueProducido.objects.all().prefetch_related('elemento_corrida__bloqueMedidas__tipo_de_espuma').prefetch_related('elemento_corrida__lote')
	context ={
		'bloques_disponibles':bloques_disponibles,
	}
	return render(request,'bloques/bloques_disponibles.html',context)

def bloque_no_disponible(request, bloque_id):
	bloque = BloqueProducido.objects.get(id=bloque_id)
	bloque.disponible = False
	bloque.save()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))