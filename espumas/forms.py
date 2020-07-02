

from django import forms
from.models import *
from django.utils.translation import gettext_lazy as _

class medidasForm(forms.ModelForm):

    def informacion_general(self):
        fields = self.visible_fields()
        return [field for field in fields if (field.name in [
        'tipo_de_espuma','tipo_de_unidad','forma','disponible','descripcion',
        'largo_frio_objetivo','ancho_frio_objetivo','alto_frio_objetivo','uso_objetivo', 'familia_de_medidas',
        ])]
    
    def parametros(self):
        fields = self.visible_fields()
        return [field for field in fields if (field.name in [
        'largo_caliente_minimo','largo_caliente_parametro_bajo','largo_caliente_setting_predefinido','largo_caliente_parametro_alto','largo_caliente_maximo',
        'ancho_caliente_minimo','ancho_caliente_parametro_bajo','ancho_caliente_setting_predefinido','ancho_caliente_parametro_alto','ancho_caliente_maximo',
        'alto_caliente_minimo','alto_caliente_parametro_bajo','alto_caliente_setting_predefinido','alto_caliente_parametro_alto','alto_caliente_maximo',
        ])]
    
    class Meta:
        model = BloqueMedidas
        fields = ['tipo_de_espuma','tipo_de_unidad','forma','disponible','descripcion','familia_de_medidas','uso_objetivo', 
        'largo_frio_objetivo','ancho_frio_objetivo','alto_frio_objetivo',
        'largo_caliente_minimo','largo_caliente_parametro_bajo','largo_caliente_setting_predefinido','largo_caliente_parametro_alto','largo_caliente_maximo',
        'ancho_caliente_minimo','ancho_caliente_parametro_bajo','ancho_caliente_setting_predefinido','ancho_caliente_parametro_alto','ancho_caliente_maximo',
        'alto_caliente_minimo','alto_caliente_parametro_bajo','alto_caliente_setting_predefinido','alto_caliente_parametro_alto','alto_caliente_maximo',
        ]
        


class tdeForm(forms.ModelForm):

    class Meta:
        model = Tipos_de_Espuma
        fields = [
        'tipo_de_espuma','formulacion_o_clave','multiplicador','precio','familia',
        'retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','disponible',
        'densidad_descripcion',
        'densidad_objetivo_minima','densidad_objetivo_baja','densidad_objetivo','densidad_objetivo_alta','densidad_objetivo_maxima',
        'dureza_objetivo_minima','dureza_objetivo_baja','dureza_objetivo','dureza_objetivo_alta','dureza_objetivo_maxima',
        'flujo_de_aire_astm_minimo','flujo_de_aire_astm_bajo','flujo_de_aire_astm_objetivo','flujo_de_aire_astm_alto','flujo_de_aire_astm_maximo',
        'flujo_de_aire_campo_minimo','flujo_de_aire_campo_bajo','flujo_de_aire_campo_objetivo','flujo_de_aire_campo_alto','flujo_de_aire_campo_maximo',
        ]
        # error_messages = {
        #     'tipo_de_espuma':{
        #         'required':'este campo es requerido compa',
        #     } 
        # }

    def informacion_general(self):
        fields = self.visible_fields()
        return [field for field in fields if (field.name in [
        'tipo_de_espuma','formulacion_o_clave','multiplicador','precio','familia',
        'retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','disponible',
        'densidad_descripcion',
        ])]
    
    def parametros(self):
        fields = self.visible_fields()
        return [field for field in fields if (field.name in [
        'densidad_objetivo_minima','densidad_objetivo_baja','densidad_objetivo','densidad_objetivo_alta','densidad_objetivo_maxima',
        'dureza_objetivo_minima','dureza_objetivo_baja','dureza_objetivo','dureza_objetivo_alta','dureza_objetivo_maxima',
        'flujo_de_aire_astm_minimo','flujo_de_aire_astm_bajo','flujo_de_aire_astm_objetivo','flujo_de_aire_astm_alto','flujo_de_aire_astm_maximo',
        'flujo_de_aire_campo_minimo','flujo_de_aire_campo_bajo','flujo_de_aire_campo_objetivo','flujo_de_aire_campo_alto','flujo_de_aire_campo_maximo',
        ])]
    