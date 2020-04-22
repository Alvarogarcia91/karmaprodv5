from django.contrib import admin


from .models import *



class CorridaAdmin(admin.ModelAdmin):
    list_display = ['id','created','pre_orden','pendiente_produccion','en_produccion','cancelada','producto_terminado','fecha_programada',]
    list_editable = ['pre_orden','pendiente_produccion','en_produccion','cancelada','producto_terminado']
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(Corrida,CorridaAdmin)

class ElementoCorridaAdmin(admin.ModelAdmin):
    list_display = ['created','bloqueMedidas','corrida','cantidad',]
    #list_editable = []
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(ElementoCorrida,ElementoCorridaAdmin)

class BloqueProducidoAdmin(admin.ModelAdmin):
    list_display = ['created', 'no_de_bloque','elemento_corrida', 'revision_calidad', 'defecto', 'alto_caliente', 'peso_caliente', 'flujo_de_aire_caliente',]
    #list_editable = []
    # prepopulated_fields = {'slug':('name',)}
admin.site.register(BloqueProducido,BloqueProducidoAdmin)