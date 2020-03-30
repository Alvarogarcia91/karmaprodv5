

from django import forms
from.models import *

class medidasForm(forms.ModelForm):
    class Meta:
        model = BloqueMedidas
        fields = ['tipo_de_espuma','tipo_de_unidad','forma','medida_dispobible','descripcion','ancho_frio_objetivo','largo_frio_objetivo','alto_frio_objetivo','flujo_de_aire_objetivo','ancho_caliente_setting_predefinido','largo_caliente_setting_predefinido','alto_caliente_setting_predefinido','cliente',]
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            # 'tipo_de_espuma': forms.ChoiceField(),
            #'tipo_de_unidad': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'forma': forms.NumberInput(attrs={'class': 'form-control'}),
            'largo_frio_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'ancho_frio_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'alto_frio_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'flujo_de_aire_objetivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'largo_caliente_setting_predefinido': forms.NumberInput(attrs={'class': 'form-control'}),
            'ancho_caliente_setting_predefinido': forms.NumberInput(attrs={'class': 'form-control'}),
            'alto_caliente_setting_predefinido': forms.NumberInput(attrs={'class': 'form-control'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            
        }
        


class tdeForm(forms.ModelForm):
    class Meta:
        model = Tipos_de_Espuma
        fields = ['tipo_de_espuma','formulacion_o_clave','multiplicador','precio','familia','densidad_descripcion','densidad_objetivo_minima','densidad_objetivo_maxima','dureza_objetivo_minima','dureza_objetivo_maxima','Flujo_de_aire_minimo','flujo_de_aire_maximo','retardante_flama','anti_bacterial','anti_estatica','color','elongacion','histasis','sag_factor','disponible']
        widgets = {
            'tipo_de_espuma': forms.TextInput(attrs={'class': 'form-control'}),
            'formulacion_o_clave': forms.TextInput(attrs={'class': 'form-control'}),
            'multiplicador': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'familia': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'densidad_descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'densidad_objetivo_minima': forms.NumberInput(attrs={'class': 'form-control'}),
            'densidad_objetivo_maxima': forms.NumberInput(attrs={'class': 'form-control'}),
            'dureza_objetivo_minima': forms.NumberInput(attrs={'class': 'form-control'}),
            'dureza_objetivo_maxima': forms.NumberInput(attrs={'class': 'form-control'}),
            'Flujo_de_aire_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'flujo_de_aire_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'retardante_flama': forms.TextInput(attrs={'class': 'form-control'}),
            'anti_bacterial': forms.TextInput(attrs={'class': 'form-control'}),
            'anti_estatica': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'elongacion': forms.TextInput(attrs={'class': 'form-control'}),
            'histasis': forms.TextInput(attrs={'class': 'form-control'}),
            'sag_factor': forms.TextInput(attrs={'class': 'form-control'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-control'}),

        }
