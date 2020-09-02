from django.urls import path
from . import views

app_name='corrida'

urlpatterns = [

    #aqui defines el tipo y nombre  del parametro que le mandas al view

    path('nueva/', views.nueva_corrida, name='nueva_corrida'),
    path('nueva/<int:forma_id>/', views.nueva_corrida, name='nueva_corrida'),
    path('nueva/<int:forma_id>/<int:tipo_de_espuma_id>', views.nueva_corrida, name='nueva_corrida'),

    path('add/<int:bloque_medidas_id>/', views.agrega_a_corrida, name='agregar_a_corrida'),
    path('orden/', views.orden_de_corrida, name='orden_de_corrida'),
    path('remover_elemento_corrida/<int:elemento_id>/', views.remover_elemento_corrida, name='remover_elemento_corrida'),

    path('cancelar_corrida/<int:corrida_id>/', views.cancelar_corrida, name='cancelar_corrida'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('ordenes_pendientes/', views.ordenes_pendientes, name='ordenes_pendientes'),
    path('producir_corrida/<int:corrida_id>/', views.producir_corrida, name='producir_corrida'),
    path('producir_bloques/<int:corrida_id>/', views.producir_bloques, name='producir_bloques'),
    path('producir_bloques/<int:corrida_id>/<int:elementoCorrida_id>/', views.producir_bloques, name='producir_bloques'),
    # path('producir_bloques/<int:corrida_id>/<int:elementoCorrida_id>/', views.producir_bloques, name='producir_bloques'),
    path('producir_bloque_seleccionado/', views.producir_bloque_seleccionado, name='producir_bloque_seleccionado'),
    
    path('editar_cantidades_corrida/', views.editar_cantidades_corrida, name='editar_cantidades_corrida'),

    path('corrida_producida/<int:corrida_id>/', views.corrida_producida, name='corrida_producida'),

    path('monitoreo/<int:corrida_id>/', views.monitoreo_de_produccion, name='monitoreo'),

    path('corridas_producidas/', views.corridas_producidas, name='corridas_producidas'),

    path('inventario/', views.inventario, name='inventario'),

    path('lotes/', views.lotes, name='lotes'),

    path('aprobar_lote/<int:lote_id>/', views.aprobar_lote, name='aprobar_lote'),

    path('dashboard/', views.dashboard_en_producion, name='dashboard'),

    path('bloques_disponibles/', views.bloques_disponibles, name='bloques_disponibles'),

    path('bloque_no_disponible/<int:bloque_id>', views.bloque_no_disponible, name='bloque_no_disponible'),


]
