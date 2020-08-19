from django.contrib import admin
from .models import *


class TiposDeEspumaAdmin(admin.ModelAdmin):
    list_display = ['tipo_de_espuma','formulacion_o_clave','multiplicador','precio','familia','disponible',
    'densidad_objetivo','densidad_descripcion','densidad_objetivo_maxima','densidad_objetivo_minima','densidad_objetivo_alta','densidad_objetivo_baja',
    'dureza_objetivo','densidad_objetivo_maxima','dureza_objetivo_minima','dureza_objetivo_alta','dureza_objetivo_baja',
    'flujo_de_aire_astm_maximo','flujo_de_aire_astm_minimo','flujo_de_aire_astm_bajo','flujo_de_aire_astm_alto',
    'flujo_de_aire_campo_maximo','flujo_de_aire_campo_minimo','flujo_de_aire_campo_bajo','flujo_de_aire_campo_alto',
    'retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','extra1','extra2',]
    list_editable = ['formulacion_o_clave','multiplicador','precio','familia','disponible',
    'densidad_objetivo','densidad_descripcion','densidad_objetivo_maxima','densidad_objetivo_minima','densidad_objetivo_alta','densidad_objetivo_baja',
    'dureza_objetivo','densidad_objetivo_maxima','dureza_objetivo_minima','dureza_objetivo_alta','dureza_objetivo_baja',
    'flujo_de_aire_astm_maximo','flujo_de_aire_astm_minimo','flujo_de_aire_astm_bajo','flujo_de_aire_astm_alto',
    'flujo_de_aire_campo_maximo','flujo_de_aire_campo_minimo','flujo_de_aire_campo_bajo','flujo_de_aire_campo_alto',
    'retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','extra1','extra2',]
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Tipos_de_Espuma,TiposDeEspumaAdmin)


class FormasAdmin(admin.ModelAdmin):
    list_display = ['forma']
    #list_editable = []
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Formas,FormasAdmin)


class TiposDeUnidadAdmin(admin.ModelAdmin):
    list_display = ['tipo_de_unidad']
    #list_editable = []
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Tipos_de_Unidad,TiposDeUnidadAdmin)


class BloqueMedidasdAdmin(admin.ModelAdmin):
    list_display = ['id','familia_de_medidas','descripcion','tipo_de_espuma','tipo_de_unidad','forma','largo_frio_objetivo','ancho_frio_objetivo','alto_frio_objetivo','largo_caliente_setting_predefinido','largo_caliente_maximo','largo_caliente_minimo','largo_caliente_parametro_alto','largo_caliente_parametro_bajo' ,'ancho_caliente_setting_predefinido','ancho_caliente_maximo','ancho_caliente_minimo','ancho_caliente_parametro_alto','ancho_caliente_parametro_bajo','alto_caliente_setting_predefinido','alto_caliente_maximo','alto_caliente_minimo','alto_caliente_parametro_alto','alto_caliente_parametro_bajo','uso_objetivo','disponible','created','updated']
    list_editable = ['descripcion','largo_frio_objetivo','ancho_frio_objetivo','alto_frio_objetivo','largo_caliente_setting_predefinido','largo_caliente_maximo','largo_caliente_minimo','largo_caliente_parametro_alto','largo_caliente_parametro_bajo' ,'ancho_caliente_setting_predefinido','ancho_caliente_maximo','ancho_caliente_minimo','ancho_caliente_parametro_alto','ancho_caliente_parametro_bajo','alto_caliente_setting_predefinido','alto_caliente_maximo','alto_caliente_minimo','alto_caliente_parametro_alto','alto_caliente_parametro_bajo','uso_objetivo','disponible']
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(BloqueMedidas,BloqueMedidasdAdmin)
