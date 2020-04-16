from django.contrib import admin
from .models import *


class TiposDeEspumaAdmin(admin.ModelAdmin):
    list_display = ['tipo_de_espuma','formulacion_o_clave','multiplicador','precio','familia','disponible','densidad_descripcion',
    'densidad_objetivo_minima','densidad_objetivo_maxima','dureza_objetivo_minima','densidad_objetivo_maxima','dureza_objetivo_minima','dureza_objetivo_maxima','Flujo_de_aire_minimo','flujo_de_aire_maximo','retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','extra1','extra2',]
    list_editable = ['formulacion_o_clave','multiplicador','precio','familia','disponible','densidad_descripcion',
    'densidad_objetivo_minima','densidad_objetivo_maxima','dureza_objetivo_minima','densidad_objetivo_maxima','dureza_objetivo_minima','dureza_objetivo_maxima','Flujo_de_aire_minimo','flujo_de_aire_maximo','retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','extra1','extra2',]
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
    list_display = ['id','descripcion','tipo_de_espuma','tipo_de_unidad','forma','largo_frio_objetivo','ancho_frio_objetivo','alto_frio_objetivo','flujo_de_aire_objetivo','largo_caliente_setting_predefinido','ancho_caliente_setting_predefinido','alto_caliente_setting_predefinido','uso_objetivo','medida_dispobible','created','updated']
    list_editable = ['descripcion','largo_frio_objetivo','ancho_frio_objetivo','alto_frio_objetivo','flujo_de_aire_objetivo','largo_caliente_setting_predefinido','ancho_caliente_setting_predefinido','alto_caliente_setting_predefinido','uso_objetivo','medida_dispobible',]
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(BloqueMedidas,BloqueMedidasdAdmin)
