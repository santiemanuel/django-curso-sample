from ..models import Estudiante
from django import forms

class BusquedaEstudianteForm(forms.ModelForm):
    apellido = forms.CharField(max_length=50, required=False, label="Apellido del estudiante")

    class Meta:
        model = Estudiante
        exclude = ['nombre', 'email']

class EstudianteForm(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ['nombre', 'email']
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo'})
        }




