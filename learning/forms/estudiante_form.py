from ..models import Estudiante
from django import forms

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




