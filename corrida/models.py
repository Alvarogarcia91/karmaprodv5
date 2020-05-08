from django.db import models
from espumas.models import BloqueMedidas
from django.db.models import Sum
import datetime
from decimal import *

class Corrida(models.Model):
	#corrida_id = models.CharField(max_length=250, blank=True)
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	pre_orden = models.BooleanField(default = True)
	pendiente_produccion = models.BooleanField(default = False)
	en_produccion = models.BooleanField(default = False)
	cancelada = models.BooleanField(default = False)
	producto_terminado = models.BooleanField(default = False)
	fecha_programada = models.DateTimeField(null = True)


	class Meta:
		db_table = 'Corrida'
		ordering = ['-id']

	def total_de_bloques(self):
		return ElementoCorrida.objects.filter(corrida = self).aggregate(Sum('cantidad'))

	def __str__(self):
		return str(self.pk)

class Lote(models.Model):	
	created = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField(auto_now = True)
	no_de_lote = models.CharField(max_length = 100)
	dureza_capturada = models.DecimalField(max_digits = 10, decimal_places = 2)
	sag_factor_capturado = models.DecimalField(max_digits = 10, decimal_places = 2)
	densidad_capturada = models.DecimalField(max_digits = 10, decimal_places = 2)
	flujo_de_aire_astm_capturado = models.DecimalField(max_digits = 10, decimal_places = 2)
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
	lote = models.ForeignKey(Lote, on_delete=models.CASCADE)
	bloqueMedidas = models.ForeignKey(BloqueMedidas, on_delete = models.CASCADE)
	corrida = models.ForeignKey(Corrida, on_delete = models.CASCADE)
	cantidad = models.IntegerField()
	# turno = models.IntegerField()
	#active = models.BooleanField(default=True)

	class Meta:
		db_table = 'ElementoCorrida'

	def sub_total(self):
		return self.bloqueMedidas.price * self.cantidad

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
		('fdm', 'Fuera de medida'),
		('a', 'Algodonozo'),
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
	#active = models.BooleanField(default=True)

	class Meta:
		db_table = 'BloqueProducido'
	
	def save(self, *args, **kwargs):
		# no_de_bloque
		bloques_en_corrida = BloqueProducido.objects.filter(elemento_corrida__corrida_id = self.elemento_corrida.corrida_id).count()
		self.no_de_bloque = bloques_en_corrida + 1
		
		# lote
		bloques_en_elemento_corrida = BloqueProducido.objects.filter(elemento_corrida_id = self.elemento_corrida.id).count()
		if bloques_en_elemento_corrida == 0:
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

		# volumen
		volumen = round((self.alto_caliente * self.elemento_corrida.bloqueMedidas.largo_caliente_setting_predefinido * self.elemento_corrida.bloqueMedidas.ancho_caliente_setting_predefinido)/1000000,2)
		self.volumen = volumen

		# densidad
		peso = float(self.peso_caliente)
		densidad = round((peso) / (volumen),2)
		self.densidad = densidad

		# save
		super().save(*args, **kwargs)

	def densidad_color(self):
		tipo_de_espuma =  self.elemento_corrida.bloqueMedidas.tipo_de_espuma
		maxima = tipo_de_espuma.densidad_objetivo_maxima
		minima = tipo_de_espuma.densidad_objetivo_minima
		alta = tipo_de_espuma.densidad_objetivo_alta
		baja = tipo_de_espuma.densidad_objetivo_baja
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'

		if maxima and minima and alta and baja:
			if self.densidad >= baja and self.densidad <= alta:
				return gris 
			if (self.densidad >= minima and self.densidad <= baja) or (self.densidad >= alta and self.densidad <= maxima):
				return amarillo
			if self.densidad <= minima or self.densidad >= maxima:
				return rojo
		else:
			return gris
		


	def largo_caliente_color(self):
		largo_caliente_setting_predefinido =  self.elemento_corrida.bloqueMedidas
		maxima = largo_caliente_setting_predefinido.largo_caliente_maximo
		minima = largo_caliente_setting_predefinido.largo_caliente_minimo
		alta = largo_caliente_setting_predefinido.largo_caliente_parametro_alto
		baja = largo_caliente_setting_predefinido.largo_caliente_parametro_bajo
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
	

		if maxima and minima and alta and baja:
			if self.largo_caliente >= baja and self.largo_caliente <= alta:
				return gris 
			if (self.largo_caliente >= minima and self.largo_caliente <= baja) or (self.largo_caliente >= alta and self.largo_caliente <= maxima):
				return amarillo
			if self.largo_caliente <= minima or self.largo_caliente >= maxima:
				return rojo
		else:
			return gris

	
	def ancho_caliente_color(self):
		ancho_caliente_setting_predefinido =  self.elemento_corrida.bloqueMedidas
		maxima = ancho_caliente_setting_predefinido.ancho_caliente_maximo
		minima = ancho_caliente_setting_predefinido.ancho_caliente_minimo
		alta = ancho_caliente_setting_predefinido.ancho_caliente_parametro_alto
		baja = ancho_caliente_setting_predefinido.ancho_caliente_parametro_bajo
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
	

		if maxima and minima and alta and baja:
			if self.ancho_caliente > baja and self.ancho_caliente < alta:
				return gris 
			if (self.ancho_caliente > minima and self.ancho_caliente < baja) or (self.ancho_caliente > alta and self.ancho_caliente < maxima):
				return amarillo
			if self.ancho_caliente < minima or self.ancho_caliente > maxima:
				return rojo
		else:
			return gris


	def alto_caliente_color(self):
		alto_caliente_setting_predefinido =  self.elemento_corrida.bloqueMedidas
		maxima = alto_caliente_setting_predefinido.alto_caliente_maximo
		minima = alto_caliente_setting_predefinido.alto_caliente_minimo
		alta = alto_caliente_setting_predefinido.alto_caliente_parametro_alto
		baja = alto_caliente_setting_predefinido.alto_caliente_parametro_bajo
		amarillo = 'warning'
		gris = 'secondary'
		rojo = 'danger'
	

		if maxima and minima and alta and baja:
			if self.alto_caliente > baja and self.alto_caliente < alta:
				return gris 
			if (self.alto_caliente > minima and self.alto_caliente < baja) or (self.alto_caliente > alta and self.alto_caliente < maxima):
				return amarillo
			if self.alto_caliente < minima or self.alto_caliente > maxima:
				return rojo
		else:
			return gris
		
	
	def flujo_de_aire_caliente_color(self):
		tipo_de_espuma =  self.elemento_corrida.bloqueMedidas.tipo_de_espuma
	
		



	def __str__(self):
		return 'Alto: {0} | Peso: {1} | F.Aire: {2}  '   .format(self.alto_caliente, self.peso_caliente,self.flujo_de_aire_caliente)