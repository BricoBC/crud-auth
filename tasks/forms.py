from django.forms import ModelForm
#Clase que hace herencia para crear un forms

from .models import Task
#La tabla con la que se va hacer un forms.

class TaskForm(ModelForm):
    class Meta:
        model = Task
        #Tabla
        fields = ['title', 'description', 'important']
        # Se agrega los campos que se quiere hacer el formulario
