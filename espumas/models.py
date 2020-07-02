from django.db import models


#modelo de tipo de espuma
class Tipos_de_Espuma(models.Model):

    tipo_de_espuma =models.CharField(max_length = 200)
    formulacion_o_clave = models.CharField(max_length = 200,blank = True)
    multiplicador = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null=True)
    precio = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True)
    familia= models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True)

    disponible = models.BooleanField(default = True)

    densidad_objetivo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)

    densidad_descripcion = models.CharField(max_length = 200,blank = True)
    densidad_objetivo_maxima = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null=True)
    densidad_objetivo_minima = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null=True)
    densidad_objetivo_alta = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null=True)
    densidad_objetivo_baja = models.DecimalField(max_digits = 10, decimal_places = 2, blank = True, null=True)

    dureza_objetivo = models.DecimalField(max_digits=10, decimal_places = 2,blank = True, null=True)
    dureza_objetivo_maxima = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True)
    dureza_objetivo_minima = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True)
    dureza_objetivo_alta = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True)
    dureza_objetivo_baja = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True)
   
    flujo_de_aire_astm_objetivo = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_astm_maximo = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_astm_minimo = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_astm_alto = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_astm_bajo = models.DecimalField(max_digits = 10, decimal_places = 2,blank = True, null = True) 

    flujo_de_aire_campo_objetivo = models.DecimalField(max_digits=10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_campo_maximo = models.DecimalField(max_digits=10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_campo_minimo = models.DecimalField(max_digits=10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_campo_alto = models.DecimalField(max_digits=10, decimal_places = 2,blank = True, null = True) 
    flujo_de_aire_campo_bajo = models.DecimalField(max_digits=10, decimal_places = 2,blank = True, null = True) 


    retardante_flama = models.CharField(max_length = 200, blank = True)
    anti_bacterial =models.CharField(max_length = 200, blank = True)
    anti_estatica =models.CharField(max_length = 200, blank = True)
    color =models.CharField(max_length = 200, blank = True)
    elongacion =models.CharField(max_length = 200, blank = True)
    histasis =models.CharField(max_length = 200, blank = True)
    sag_factor =models.CharField(max_length = 200, blank = True)
    extra1 =models.CharField(max_length = 200, blank = True)
    extra2 =models.CharField(max_length = 200, blank = True)

    

    class Meta:
        ordering = ('tipo_de_espuma',)
        verbose_name = 'TipodeEspuma'
        verbose_name_plural = 'Tipos_de_Espuma'

    def __str__(self):
        return '{}'.format(self.tipo_de_espuma)


#formas de block (Block , Cilindro , Cajon)
class Formas(models.Model):
    forma = models.CharField(max_length=200)
    class Meta:
        ordering = ('pk',)
        verbose_name = 'forma'
        verbose_name_plural = 'formas'

    def __str__(self):
        return self.forma


#tipos de unidades (Inicio,Normal,Cambio,Final,Muestra)
class Tipos_de_Unidad(models.Model):
    tipo_de_unidad = models.CharField(max_length=200)
    class Meta:
        ordering = ('pk',)
        verbose_name = 'Tipo de unidad'
        verbose_name_plural = 'Tipos de unidades'

    def __str__(self):
        return self.tipo_de_unidad



#BloqueMedidas es el block que se producira , tiene tipo de espuma forma unidad y sus medidas a producirs
class BloqueMedidas(models.Model):

    descripcion = models.CharField(max_length = 200, blank = False,null = False)
    tipo_de_espuma = models.ForeignKey(Tipos_de_Espuma, on_delete = models.CASCADE)
    tipo_de_unidad = models.ForeignKey(Tipos_de_Unidad,on_delete = models.CASCADE)
    forma = models.ForeignKey(Formas,on_delete = models.CASCADE)
    familia_de_medidas = models.CharField(max_length = 10, blank = True, null = True)

    largo_frio_objetivo = models.DecimalField(max_digits=10, decimal_places=2,blank = False, null=True)
    ancho_frio_objetivo = models.DecimalField(max_digits=10, decimal_places=2,blank = False, null=True)
    alto_frio_objetivo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)

    
    largo_caliente_setting_predefinido = models.DecimalField(max_digits=10, decimal_places=2,blank = False, null=True)
    largo_caliente_maximo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    largo_caliente_minimo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    largo_caliente_parametro_alto = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    largo_caliente_parametro_bajo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)


    ancho_caliente_setting_predefinido = models.DecimalField(max_digits=10, decimal_places=2,blank = False, null=True)
    ancho_caliente_maximo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    ancho_caliente_minimo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    ancho_caliente_parametro_alto = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    ancho_caliente_parametro_bajo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    

    alto_caliente_setting_predefinido = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    alto_caliente_maximo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    alto_caliente_minimo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    alto_caliente_parametro_alto = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)
    alto_caliente_parametro_bajo = models.DecimalField(max_digits=10, decimal_places=2,blank = True, null=True)

   
    uso_objetivo  = models.CharField(max_length=200, blank=True,null=True)

    disponible =models.BooleanField(default = True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        ordering = ('familia_de_medidas','tipo_de_espuma','tipo_de_unidad')
        verbose_name = 'Bloque Medidas'
        verbose_name_plural = 'Bloques Medidas'

    def __str__(self):
        return '{}'.format(self.descripcion)
