from django.urls import path
from . import views

app_name='espumas'

urlpatterns = [
    #http://127.0.0.1:8000/espumas/
    path('', views.espumas, name='espumas'),
    #http://127.0.0.1:8000/espumas/respuesta
    path('respuesta', views.respuesta, name='respuesta'),


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
