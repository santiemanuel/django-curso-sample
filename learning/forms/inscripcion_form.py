from ..models import Inscripcion
from django import forms


class InscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion
        fields = ['estudiante', 'curso']
        labels = {
            'estudiante': 'Estudiante',
            'curso': 'Curso',
        }
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
        }
