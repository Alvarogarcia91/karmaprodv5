from django.contrib import admin


from .models import *



class CorridaAdmin(admin.ModelAdmin):
    list_display = ['id','created','pre_orden','pendiente_produccion','en_produccion','cancelada','producto_terminado','fecha_programada',]
    list_editable = ['pre_orden','pendiente_produccion','en_produccion','cancelada','producto_terminado']
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Corrida,CorridaAdmin)

class LoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'created','no_de_lote','dureza_capturada','sag_factor_capturado','densidad_capturada','flujo_de_aire_astm_capturado','pruebas_realizadas','pruebas_pasadas']
    list_editable = ['pruebas_realizadas','pruebas_pasadas']
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Lote,LoteAdmin)

class ElementoCorridaAdmin(admin.ModelAdmin):
    list_display = ['id', 'created','lote_id','bloqueMedidas','corrida','cantidad',]
    #list_editable = []
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(ElementoCorrida,ElementoCorridaAdmin)

class BloqueProducidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'disponible', 'created', 'no_de_bloque','elemento_corrida', 'revision_calidad', 'defecto', 'alto_caliente', 'peso_caliente', 'flujo_de_aire_caliente','volumen','densidad',]
    #list_editable = []
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(BloqueProducido,BloqueProducidoAdmin)