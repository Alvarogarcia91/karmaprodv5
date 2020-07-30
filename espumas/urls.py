from django.urls import path
from . import views

app_name='espumas'

urlpatterns = [
    #----PANTALLA PARA AGREGAR A ORDEN DE CORRIDA---
    #http://127.0.0.1:8000/espumas/
    path('', views.espumas, name='espumas'),

    #http://127.0.0.1:8000/espumas/respuesta
    path('respuesta', views.respuesta, name='respuesta'),


    #------CRUD MEDIDAS----
    #http://127.0.0.1:8000/espumas/medidas
    path('medidas/', views.medidas, name='medidas'),
    path('medidas/<int:tipo_id>/',views.medidas,name='medidas_filtrado'),

    #http://127.0.0.1:8000/espumas/1/
    path('<int:item_id>/',views.detalle_medidas,name='detalle_medidas'),
    #http://127.0.0.1:8000/espumas/agregarmedida
    path('agregarmedida',views.agregar_medidas,name='agregar_medidas'),
    #http://127.0.0.1:8000/espumas/editarmedida/1
    path('editarmedida/<int:id>',views.editar_medidas,name='editar_medidas'),
    #http://127.0.0.1:8000/espumas/deletemedida/1
    path('deletemedida/<int:id>',views.borrar_medidas,name='borrar_medidas'),


    #----Display y CRUD de TDE----
    #http://127.0.0.1:8000/espumas/tde/
    path('tde/', views.tde, name='tde'),
    #http://127.0.0.1:8000/espumas/tde/1/
    path('tde/<int:item_id>/',views.detalle_tde,name='detalle_tde'),
    #http://127.0.0.1:8000/espumas/agregartde
    path('agregartde',views.agregar_tde,name='agregar_tde'),
    #http://127.0.0.1:8000/espumas/editartde/1
    path('editartde/<int:id>',views.editar_tde,name='editar_tde'),
    #http://127.0.0.1:8000/espumas/deletetde/3
    path('deletetde/<int:id>',views.borrar_tde,name='borrar_tde'),
   
    #http://127.0.0.1:8000/espumas/medidas  
    path('formas/', views.formas, name='formas'),


#     path('sand1/', views.sand1, name='sand1'),
#     path('sand2/', views.sand2, name='sand2'),
#     path('checkout/',views.checkout,name='checkout'),
#     #app/numero
#     #OJO item_id es la var que declaraste en views
#     path('<int:item_id>/',views.detalle,name='detalle'),
#
#     #agregar
#     path('agregarmedida',views.agregar_medidas,name='agregar_medidas'),
#
#
#     #editar
#     # path('editar/<int:id>/', views.editar_medidas,name='editar_medidas')
#     path('editar/<int:id>',views.editar_medidas,name='editar_medidas'),
#
#     #borrar
#     path('delete/<int:id>',views.borrar_medidas,name='borrar_medidas'),
#
#
# #####
#     #sand de drop down nuevo
#     path('sand3/', views.sand3, name='sand3'),
#




    # path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
    # path('<slug:c_slug>/<slug:product_slug>/', views.ProdCatDetail, name='ProdCatDetail'),
    # path('pruebadisplays', views.pruebadisplays, name='pruebadisplays'),


]
