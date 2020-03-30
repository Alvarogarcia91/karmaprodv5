from django.urls import path
from . import views

app_name='corrida'

urlpatterns = [

    #aqui defines el tipo y nombre  del parametro que le mandas al view

	path('add/<int:bloque_medidas_id>/', views.agrega_a_corrida, name='agregar_a_corrida'),
    path('orden/', views.orden_de_corrida, name='orden_de_corrida'),
	path('remover_elemento_catalogo/<int:elemento_id>/', views.remover_elemento_catalogo, name='remover_elemento_catalogo'),
    path('remover_elemento_ordenes/<int:elemento_id>/', views.remover_elemento_ordenes, name='remover_elemento_ordenes'),
    path('remover_elemento_ordenes_pendientes/<int:elemento_id>/', views.remover_elemento_ordenes_pendientes, name='remover_elemento_ordenes_pendientes'),

    path('cancelar_corrida/<int:corrida_id>/', views.cancelar_corrida, name='cancelar_corrida'),
    path('ordenes/', views.ordenes, name='ordenes'),
    path('ordenes_pendientes/', views.ordenes_pendientes, name='ordenes_pendientes'),
    path('producir_corrida/<int:corrida_id>/', views.producir_corrida, name='producir_corrida'),
    path('producir_bloques/<int:corrida_id>/', views.producir_bloques, name='producir_bloques'),
    path('producir_bloques/<int:corrida_id>/<int:elementoCorrida_id>/', views.producir_bloques, name='producir_bloques'),
    path('producir_bloques/<int:corrida_id>/<int:elementoCorrida_id>/', views.producir_bloques, name='producir_bloques'),
    path('producir_bloque_seleccionado/', views.producir_bloque_seleccionado, name='producir_bloque_seleccionado'),
    
    path('editar_cantidades_corrida/', views.editar_cantidades_corrida, name='editar_cantidades_corrida'),
]
