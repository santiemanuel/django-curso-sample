from ..models import Estudiante
from django import forms

class BusquedaEstudianteForm(forms.ModelForm):
    apellido = forms.CharField(max_length=50, required=False, label="Apellido del estudiante")

    class Meta:
        model = Estudiante
        exclude = ['nombre', 'email']

class EstudianteFormPasoUno(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ['nombre', 
                  'email',
                  'avatar',
                  'dob',]

        labels = {
            'nombre': 'Nombre',
            'email': 'Correo electrónico',
            'avatar': 'Imagen de perfil',
            'dob': 'Fecha de nacimiento',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese su nombre', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ingrese su correo', 'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'placeholder': 'Seleccione una imagen de perfil', 'class': 'form-control'}),
            'dob': forms.NumberInput(attrs={'type':'date', 'placeholder': 'Ingrese la fecha de nacimiento', 'class': 'form-control'}),
        }

class EstudianteFormPasoDos(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ['nivel_educativo', 
                  'interest',
                  'habilidades',]

        labels = {
            'nivel_educativo': 'Nivel educativo',
            'interest': 'Intereses',
            'habilidades': 'Habilidades',
        }
        widgets = {
            'nivel_educativo': forms.Select(attrs={'placeholder': 'Seleccione su nivel educativo', 'class': 'form-control'}),
            'interest': forms.Textarea(attrs={'placeholder': 'Ingrese sus intereses', 'class': 'form-control'}),
            'habilidades': forms.Textarea(attrs={'placeholder': 'Ingrese sus habilidades', 'class': 'form-control'}),
        }

class EstudianteFormPasoTres(forms.ModelForm):

    class Meta:
        model = Estudiante
        fields = ['bio', 
                  'github',
                  'facebook',]

        labels = {
            'bio': 'Biografía',
            'github': 'GitHub',
            'facebook': 'Facebook',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Ingrese su biografía', 'class': 'form-control'}),
            'github': forms.URLInput(attrs={'placeholder': 'Ingrese su perfil de GitHub', 'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'placeholder': 'Ingrese su perfil de Facebook', 'class': 'form-control'}),
        }



