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
        fields = ['nombre', 
                  'email',
                  'avatar',
                  'dob',
                  'bio',
                  'interest',
                  'github']

        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'avatar': 'Imagen de perfil',
            'dob': 'Fecha de nacimiento',
            'bio': 'Biografía',
            'interest': 'Intereses',
            'github': 'GitHub',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo', 'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'placeholder': 'Seleccione una imagen de perfil', 'class': 'form-control'}),
            'dob': forms.NumberInput(attrs={'type':'date', 'placeholder': 'Ingrese la fecha de nacimiento', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'interest': forms.Textarea(attrs={'class': 'form-control'}),
            'github': forms.URLInput(attrs={'class': 'form-control'}),
        }




