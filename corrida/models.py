from django.db import models
from espumas.models import BloqueMedidas
from django.db.models import Sum
import datetime
from decimal import *

class Corrida(models.Model):
	#corrida_id = models.CharField(max_length=250, blank=True)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	fecha_programada = models.DateTimeField(null = True)
	fecha_creacion = models.DateTimeField(null = True)
	fecha_produccion = models.DateTimeField(null = True)
	pre_orden = models.BooleanField(default = True)
	pendiente_produccion = models.BooleanField(default = False)
	en_produccion = models.BooleanField(default = False)
	cancelada = models.BooleanField(default = False)
	producto_terminado = models.BooleanField(default = False)
	
	class Meta:
		db_table = 'Corrida'
		ordering = ['-id']

	def area_de_curado_estimada(self):
		elementos = self.elementocorrida_set.all()
		area_total = 0
		for elemento in elementos:
			largo = float(elemento.bloqueMedidas.largo_caliente_setting_predefinido) or 0
			ancho = float(elemento.bloqueMedidas.ancho_caliente_setting_predefinido)or 0
			area_bloque = ((largo/100) + 0.1) * ((ancho/100) + 0.1)
			area_elemento = area_bloque * elemento.cantidad
			area_total = area_total + area_elemento
		
		return round(area_total,2)

	def area_de_curado(self):
		elementos = self.elementocorrida_set.all()
		area_total = 0
		for elemento in elementos:
			area_elemento = elemento.area_de_curado()
			area_total = area_total + area_elemento
		return round(area_total,2)


	def total_de_bloques(self):
		return ElementoCorrida.objects.filter(corrida = self).aggregate(Sum('cantidad'))

	def __str__(self):
		return str(self.pk)

class Lote(models.Model):	
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	no_de_lote = models.CharField(max_length = 100)
	dureza_capturada = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, default= 0)
	sag_factor_capturado = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, default= 0)
	densidad_capturada = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, default= 0)
	flujo_de_aire_astm_capturado = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, default= 0)
	pruebas_realizadas = models.BooleanField(default = False)
	pruebas_pasadas = models.BooleanField(default = False)
	


	class Meta:
		db_table = 'Lote'
		# ordering = ['']

	def __str__(self):
		return str(self.no_de_lote)



class ElementoCorrida(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
	lote = models.ForeignKey(Lote, on_delete=models.CASCADE, null= True)
	bloqueMedidas = models.ForeignKey(BloqueMedidas, on_delete = models.CASCADE)
	corrida = models.ForeignKey(Corrida, on_delete = models.CASCADE)
	cantidad = models.IntegerField()
	# turno = models.IntegerField()
	#active = models.BooleanField(default=True)

	class Meta:
		db_table = 'ElementoCorrida'
		ordering = ['lote']

	def sub_total(self):
		return self.bloqueMedidas.price * self.cantidad

	def bloques_producidos(self):
		return self.bloqueproducido_set.all().count()

	def area_de_curado(self):
		bloques = self.bloqueproducido_set.all()
		area_total = 0
		bloques_count = bloques.count()
		margen_lineal = bloques_count * 0.1
		largo_total = float(bloques.aggregate(sum=Sum('largo_caliente'))['sum'] or 0)
		ancho_total = float(bloques.aggregate(sum=Sum('ancho_caliente'))['sum'] or 0)
		area_total = ((largo_total/100)+(margen_lineal)) *((ancho_total/100)+(margen_lineal))

		return area_total

	def metros_lineales_individuales(self):
		return self.bloqueMedidas.largo_frio_objetivo * self.cantidad

	def __str__(self):
		return '{0} {1},{2}'.format( self.bloqueMedidas.tipo_de_espuma, self.bloqueMedidas.descripcion, self.bloqueMedidas.tipo_de_unidad)





class BloqueProducido(models.Model):
	
	DEFECTOS_CHOICES=[
		('sd', ''),
		('ph','Pinhole'),
		('g', 'Grieta'),
		('v', 'Vena'),
		('mm','Mal manejo'),
		('fm', 'Fuera de medida'),
		('a', 'Algodonozo'),
		('ma', 'Manchado'),
	]

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
	no_de_bloque = models.IntegerField(default=1)
	elemento_corrida = models.ForeignKey(ElementoCorrida, on_delete = models.CASCADE)
	revision_calidad = models.BooleanField(default=True)
	defecto = models.CharField(max_length=2,choices=DEFECTOS_CHOICES, default='sd')
	largo_caliente = models.DecimalField(max_digits=10, decimal_places=2 ,null = True, default = 122,blank = True )
	ancho_caliente = models.DecimalField(max_digits=10, decimal_places=2,null = True,default = 122 ,blank = True)
	alto_caliente = models.DecimalField(max_digits=10, decimal_places=2,null = True , default = 122,blank = True )
	flujo_de_aire_caliente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank = True)
	peso_caliente = models.DecimalField(max_digits=10, decimal_places=2)
	comentario = models.CharField(max_length =300,blank = True,null=True)
	volumen = models.DecimalField(max_digits=10, decimal_places=2,  blank= True, null = True)
	densidad = models.DecimalField(max_digits=10, decimal_places=2, blank= True, null = True)
	disponible = models.BooleanField(default=True)

	class Meta:
		db_table = 'BloqueProducido'
	
	def save(self, *args, **kwargs):
		# no_de_bloque
		bloques_en_corrida = BloqueProducido.objects.filter(elemento_corrida__corrida_id = self.elemento_corrida.corrida_id).count()
		self.no_de_bloque = bloques_en_corrida + 1
		elemento_corrida = self.elemento_corrida
		# lote
		bloques_en_elemento_corrida = BloqueProducido.objects.filter(elemento_corrida_id = elemento_corrida.id).count()
		if bloques_en_elemento_corrida == 0:
			elemento_corrida_con_lote = ElementoCorrida.objects.filter(corrida_id = elemento_corrida.corrida_id).filter(bloqueMedidas__familia_de_medidas = elemento_corrida.bloqueMedidas.familia_de_medidas).exclude(lote__isnull=True)
			if elemento_corrida_con_lote:
				
				lote = elemento_corrida_con_lote[0].lote
			else:
				meses = {"1":"L", "2":"U", "3":"I", "4":"S", "5":"V", "6":"G", "7":"A", "8":"R", "9":"C", "10":"M", "11":"T", "12":"Z"}
				today = datetime.datetime.today()
				letra = meses[str(today.month)]
				year = str(today.year)[-2:]
				tipo_de_espuma = self.elemento_corrida.bloqueMedidas.tipo_de_espuma
				corrida = self.elemento_corrida.corrida
				corridas_en_dia = BloqueProducido.objects.filter(created__date = today).distinct('elemento_corrida__corrida_id').count() 
				if not corridas_en_dia:
					corridas_en_dia = 1
				consecutivo_anual = Corrida.objects.filter(producto_terminado = True).filter( created__year = today.year).count() + 1
				# cifrado/(3dig cons anual)(1dig #corrida)/TDE/
				no_de_lote = '{0}{1}{2}/{3:03d}{4}/{5}'.format(letra, today.day, year, consecutivo_anual, corridas_en_dia, tipo_de_espuma)
				lote = Lote.objects.create(
						no_de_lote = no_de_lote
				)
				lote.save()
			elemento_corrida.lote_id = lote.id
			elemento_corrida.save()
		
		# volumen
		if self.elemento_corrida.bloqueMedidas.forma.forma == "Cilindro":
			radio = float(self.ancho_caliente)/2
			area = (radio * radio * 3.1415)
			volumen = round((float(self.largo_caliente) * area)/1000000, 2)
		else:
			volumen = round((float(self.largo_caliente) * float(self.ancho_caliente) * float(self.alto_caliente))/(1000000),2)
		self.volumen = volumen

		# densidad
		peso = float(self.peso_caliente)
		densidad = round((peso) / (volumen),2)
		self.densidad = densidad

		# save
		super().save(*args, **kwargs)

	def densidad_class(self):
		tipo_de_espuma =  self.elemento_corrida.bloqueMedidas.tipo_de_espuma
		maxima = tipo_de_espuma.densidad_objetivo_maxima
		minima = tipo_de_espuma.densidad_objetivo_minima
		alta = tipo_de_espuma.densidad_objetivo_alta
		baja = tipo_de_espuma.densidad_objetivo_baja
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
		color_class = ''

		if maxima and minima and alta and baja:
			if self.densidad >= baja and self.densidad <= alta:
				color_class = ''
			if (self.densidad >= minima and self.densidad < baja) or (self.densidad > alta and self.densidad <= maxima):
				color = amarillo
				color_class ='badge badge-{0} badge-pill'.format(color)
			if self.densidad < minima or self.densidad > maxima:
				color = rojo
				color_class ='badge badge-{0} badge-pill'.format(color)
		
		return color_class


	def largo_caliente_class(self):
		bloqueMedidas =  self.elemento_corrida.bloqueMedidas
		maxima = bloqueMedidas.largo_caliente_maximo
		minima = bloqueMedidas.largo_caliente_minimo
		alta = bloqueMedidas.largo_caliente_parametro_alto
		baja = bloqueMedidas.largo_caliente_parametro_bajo
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
		color_class = ''
	
		if maxima and minima and alta and baja:
			if self.largo_caliente >= baja and self.largo_caliente <= alta:
				color_class = ''
			if (self.largo_caliente >= minima and self.largo_caliente < baja) or (self.largo_caliente > alta and self.largo_caliente <= maxima):
				color = amarillo
				color_class ='badge badge-{0} badge-pill'.format(color)
			if self.largo_caliente < minima or self.largo_caliente > maxima:
				color = rojo
				color_class ='badge badge-{0} badge-pill'.format(color)
		
		return color_class

	
	def ancho_caliente_class(self):
		bloqueMedidas =  self.elemento_corrida.bloqueMedidas
		maxima = bloqueMedidas.ancho_caliente_maximo
		minima = bloqueMedidas.ancho_caliente_minimo
		alta = bloqueMedidas.ancho_caliente_parametro_alto
		baja = bloqueMedidas.ancho_caliente_parametro_bajo
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
		color_class = ''

		if maxima and minima and alta and baja:
			if self.ancho_caliente >= baja and self.ancho_caliente <= alta:
				color_class = ''
			if (self.ancho_caliente >= minima and self.ancho_caliente < baja) or (self.ancho_caliente > alta and self.ancho_caliente <= maxima):
				color = amarillo
				color_class ='badge badge-{0} badge-pill'.format(color)
			if self.ancho_caliente < minima or self.ancho_caliente > maxima:
				color = rojo
				color_class ='badge badge-{0} badge-pill'.format(color)

		return color_class


	def alto_caliente_class(self):
		bloqueMedidas =  self.elemento_corrida.bloqueMedidas
		maxima = bloqueMedidas.alto_caliente_maximo
		minima = bloqueMedidas.alto_caliente_minimo
		alta = bloqueMedidas.alto_caliente_parametro_alto
		baja = bloqueMedidas.alto_caliente_parametro_bajo
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
		color_class = ''

		if maxima and minima and alta and baja:
			if self.alto_caliente >= baja and self.alto_caliente <= alta:
				color_class = ''
			if (self.alto_caliente >= minima and self.alto_caliente < baja) or (self.alto_caliente > alta and self.alto_caliente <= maxima):
				color = amarillo
				color_class ='badge badge-{0} badge-pill'.format(color)
			if self.alto_caliente < minima or self.alto_caliente > maxima:
				color = rojo
				color_class ='badge badge-{0} badge-pill'.format(color)
		
		return color_class

	
	def flujo_de_aire_caliente_class(self):
		return 'warning'
	
		



	def __str__(self):
		return 'Alto: {0} | Peso: {1} | F.Aire: {2}  '   .format(self.alto_caliente, self.peso_caliente,self.flujo_de_aire_caliente)
