from django.db import models
from espumas.models import BloqueMedidas
from django.db.models import Sum
import datetime
from decimal import *

class Corrida(models.Model):
	#corrida_id = models.CharField(max_length=250, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
	pre_orden = models.BooleanField(default=True)
	pendiente_produccion = models.BooleanField(default=False)
	en_produccion = models.BooleanField(default=False)
	cancelada = models.BooleanField(default=False)
	producto_terminado = models.BooleanField(default=False)
	fecha_programada = models.DateTimeField(null=True)


	class Meta:
		db_table = 'Corrida'
		ordering = ['-id']

	def total_de_bloques(self):
		return ElementoCorrida.objects.filter(corrida = self).aggregate(Sum('cantidad'))

	def __str__(self):
		return str(self.pk)

class ElementoCorrida(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now = True)
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
	elemento_corrida = models.ForeignKey(ElementoCorrida, on_delete=models.CASCADE)
	revision_calidad = models.BooleanField(default=True)
	defecto = models.CharField(max_length=2,choices=DEFECTOS_CHOICES, default='sd')
	largo_caliente = models.DecimalField(max_digits=10, decimal_places=2)
	ancho_caliente = models.DecimalField(max_digits=10, decimal_places=2)
	alto_caliente = models.DecimalField(max_digits=10, decimal_places=2)
	flujo_de_aire_caliente = models.DecimalField(max_digits=10, decimal_places=2)
	peso_caliente = models.DecimalField(max_digits=10, decimal_places=2)
	comentario =models.CharField(max_length =300,blank = True,null=True)
	lote = models.CharField(max_length =50,blank = True,null=True)
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
		self.lote = '{0}{1}{2}/{3:03d}{4}/{5}'.format(letra, today.day, year, consecutivo_anual, corridas_en_dia, tipo_de_espuma)
		
		# volumen
		volumen = round((self.alto_caliente * self.elemento_corrida.bloqueMedidas.largo_caliente_setting_predefinido * self.elemento_corrida.bloqueMedidas.ancho_caliente_setting_predefinido)/1000000,2)
		self.volumen = volumen

		# densidad
		peso = float(self.peso_caliente)
		densidad = round((peso) / (volumen),2)
		self.densidad = densidad

		# save
		super().save(*args, **kwargs)

	# def volumen(self):
	# 	return round((self.alto_caliente * self.elemento_corrida.bloqueMedidas.largo_caliente_setting_predefinido * self.elemento_corrida.bloqueMedidas.ancho_caliente_setting_predefinido)/1000000,2)

	# def densidad(self):
	# 	volumen = float(self.volumen()) 
	# 	peso = float(self.peso_caliente)
	# 	return round((peso ) / (volumen),2)

	def __str__(self):
		return 'Alto: {0} | Peso: {1} | F.Aire: {2}  '   .format(self.alto_caliente, self.peso_caliente,self.flujo_de_aire_caliente)