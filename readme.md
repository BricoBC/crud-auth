# INTRODUCCIÓN
Este proyecto está basado con conocimientos básicos que se exponen en el repositorio de _**project-django**_.
Se va a mencionar conceptos que fueron mencionados en ese repositorio y se va a ir complementando con forme se vaya aumentando la dificultad.

# 1. Buenas prácticas
Recordar que las buenas prácticas consiste en:
1. Crear carpeta del proyecto.
```bash
  mkdir carpeta
```
2. Inicializar git.
```bash
  git init
```

3. Crear entorno virtual.
```python
python3 -m venv venv
```

4. Activar entorno virtual.
```bash
source ./venv/bin/activate
```
5. Hacer un documento txt en donde esten las dependencias que utilicemos.
```python
pip freeze > requirements.txt
```

6. Instalar dependencias:
```python
pip install -r requirements.txt
```

Es importante recordar que a lo largo de la vida del proyecto hay que estar guardando las dependencias.

# 2. Instalación
Hay que recordar que se tiene dos formas de instalar Django.

```python
python3 -m pip install Django
```
ó
```python
pip install django
```

Para verificar la versión es:
 ```python
django-admin --version
```

# 3. Crear el proyecto, la app y ejecutar el servidor.
## 3.1) Proyecto
El proyecto va a tener como nombre **_crud-auth_**
```python
django-admin startproject crud-auth .
```
## 3.2) App
La aplicación se va a llamar **_tasks_**
```python
pythn manage.py startapp tasks
```

## 3.3) Ejecutar el proyecto
```python
python manage.py runserver
```
# 4. Interfaz Registrarse
Cuando se crea la app hay que recordar que se tiene que vincualar con las app del proyecto, se abre la carpeta del proyecto y se va al archivo de **_settings.py_**, se busca el array con nombre de **INSTALLED_APPS** y se agrega al final la app que se hizo.
## 4.1) Crear base de datos
Para cuando se crea un nuevo modelo recordemos que se utiliza el siguiente comando:
```python
python manage.py makemigrations
```

Para crear todos los modelos es con el siguiente comando:
```python
python manage.py migrate
```

## 4.2) Crear url
Url del proyecto
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("tasks.urls"))
]
```
Url de la app
```python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup')
]
```

## 4.3) Crear vista
```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#Ésta clase nos entrega el forms para el usuario
from django.contrib.auth.models import User
#Tabla User

def signup(request):
    error = ''
    if request.method == 'GET':
        error= ''
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                error = 'Usario creado'
            except:
                error = 'Usuario ya existe'
        else:
            error = 'Las contraseñas no son iguales'
    
    # Al final retorna a la misma página y manda una cadena de texto
    return render(request, 'signup.html', {
    'forms': UserCreationForm,
    'error': error
    })

    
```

## 4.4) Crear plantilla para la vista
```html
<h1>Signup</h1>

<form method="post">
    <!-- Llave de seguridad -->
    {% csrf_token %}

    <!-- Formulario -->
    {{ forms.as_p }}
    <button>Guardar</button>
</form>
<h3>{{ error }}</h3>

```
# 5. Incorporar cookies.
Para hacer que quede registrado en las cookies hay que ingresar el siguiente módulo:
```python
from django.contrib.auth import login
```

Se integra en la función:
```python
...
        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                error = 'Usario creado'
                login(request, user)
                # Registrar en la cokie el request y el usuario.
                return redirect('/')
...
```
Para ver que ya guarden estos datos hay que inspeccionar el sitio web, en el panel que te abra te iras a Aplicación, le das clic en Cookies y se muestran todas las que tienen el sistema.

# 6. Interfaz registrarse
## 6.1) Crear url
Hasta ahora el código para el url tiene lo siguiente:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/', views.sigin, name='login')
    #Url de login
]
```

## 6.2) Crear vista
La función de la vista queda de la siguiente forma:
```python
from django.contrib.auth import login, authenticate

def sigin(request):
    error = ''
    if request.method == 'GET':
        error=''
    else: 
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password) 
        # Devuelve el nombre usuario si es que existe
        if user is None:
            error = 'Verifica usuario/contraseña'
        else:
            login(request, user)
            return redirect('/')
        
    return render(request, 'login.html', {
        'form': AuthenticationForm,
        'error': error
    })

```
## 6.3) Crear plantilla para la vista
El código queda de la siguiente forma:
```html
<h1>LOGIN</h1>

<form method="post">
    {% csrf_token %}
    
    {{form.as_p}}
    <button>Login</button>
</form>

<h3>{{error}}</h3>
```
# 7. Agregar plantilla base
Esta sección se conoce en el **project-django** como _Reutilizar plantillas_
## 7.1) Crear plantilla base
El código queda de la siguiente forma:
```django
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DJANGO CRUD</title>
</head>
<body>

    <ul>
        {% if user.is_authenticated %}
        {# Cuando se inicia sesión se crea una variable global con el nombre de user
         Por esta variable se puede saber si ya inicio sesión o no el usuario
         La variable user está relacionada con el metodo login de view #}
        <li><a href="/logout">Cerrar sesión</a></li>
        {% else %}
        <li><a href="/login">Iniciar sesión</a></li>
        {% endif %}
    </ul>
    
    {% block content %}
    {% endblock content %}

</body>
</html>
```
## 7.2) Unir la plantilla base con la vista principal

# 8. Crear el cierre de sesión.
## 8.1) Crear url 
```python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('login/', views.sigin, name='login'),
    path('logout/', views.signout, name='logout')
]
```
## 8.2) Crear vista
```python
from django.contrib.auth import login, authenticate, logout
def signout(request):
    logout(request)
    return redirect('/login')
```
## 8.3)Crear plantilla base
La plantilla es la de base.html

# 9. Modelos
## 9.1) Crear modelo
```python
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField( max_length=50 )
    # As TextInput
    description = models.TextField( blank=True )
    #As TextArea
    created = models.DateTimeField( auto_now_add=True )
    # As DateField
    date_completed = models.DateTimeField( null=True )
    important = models.BooleanField( default=False )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #on_delete = models.CASCADE is for when deleted a user their tasks also deleted
    def __str__(self) -> str:        
        #Es para la vista en la interfaz del adminstrador
        return self.title + ' <- ' + self.user.username
```
## 9.2) Crear tablas
Compilar las tablas.
```python
python manage makemigrations
```
Después para ya crear las tablas es con:
```python
python manage migrate
```

# 10. Panel de adminstrador
Para poder ver las tablas que se van creando al panel de administrador es necesario hacer lo siguiente:
1. Ir al archivo **admin.py** de la app y agregar lo siguiente:
```python
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```
2. Crear a un superusuario y su contraseña, 
```python
python manage.py createsuperuser
```
3. En el archivo de **admin.py** de la aplicación agregar lo siguiente:
```python
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```
# 11. Crear formulario a través de una tabla creada
## 11.1) Crear el forms.
Se va a crear el archivo **forms.py** y dentro se va a poner el siguiente código:
```python
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
```
## 11.2) Crear el url para el formulario
```python
...
    path('login/', views.sigin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('task/', views.task, name='tasks'),
    path('task/create/', views.task_create, name='create_task')
]
```
## 11.3) Crear la vista para el formulario
```python
from .forms import TaskForm
#Importamos el formulario

def task_create(request):
    txt = None
    if request.method == 'GET':
        txt = ''
    else:        
        print(request.POST)
        
        txt = 'Tarea creada'
    
    return render(request, 'create_task.html',{
        'form' : TaskForm,
        'text': txt
    })
```
## 11.4) Crear la plantilla para el formulario
```django
{% extends 'base.html' %}

{% block content %}

Crear tarea

<form method="POST">
    {% csrf_token %}

    {{form.as_p}}
    <button>Crear</button>

</form>

{{text}}

{% endblock content %}
```

# 12.Guardar datos en Base de datos
Para almacenar la base de datos se puede hacer de dos formas:
1. Es la forma en como se vio en el repositorio de project-django
2. Utilizando el mismo formulario se puede guardar todos los datos, quedaria de la siguiente forma:
```python
def task_create(request):
    txt = None
    if request.method == 'GET':
        txt = ''
    else:        
        try:            
            form = TaskForm(request.POST)
            # Genera el formulario
            new_task = form.save(commit=False)
            # Se almacena los datos correspondiente a su campo
            #Commit=false es para que no se guarde en una instancia de Base de Datos
            new_task.user = request.user
            #request.user es el usuario de quien inicio sesión
            new_task.save()
            #Se guarda en base de datos
            txt = 'Tarea creada'
        except:
            txt = 'No se pudo guardar los datos'
    
    return render(request, 'create_task.html',{
        'form' : TaskForm,
        'text': txt
    })

```
## 12.1) Actualizar datos en la base de datos
1. Crar el url.
```python
    ...
    path('task/create/', views.task_create, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]
```
2. Crear la vista.
```python
def task_detail(request, task_id):
txt = ''
    task = get_object_or_404(Task, pk=task_id, user=request.user) 
    #Va a obtener los datos de la tabla Tarea mediente la llave primaria
    if request.method == 'GET':    
        form = TaskForm(instance=task)
        #Crea un formulario ya con los datos rellenos
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            #Llena el formulario con la información mandada con el metodo post mediante la instancia de la tarea
            form.save()  
            #Se guarda
            return redirect('tasks')
        except:
            txt = 'Error al actualizar datos'
    return render(request, 'task.html', {'task': task, 'form': form, 'text': txt})
```
3. Crear el template.
```django
{% extends 'base.html' %}

{% block content %}
<form method="POST">
    {% csrf_token %}
    {{form.as_p}}
    <button>Actualizar</button>
</form>
{{text}}
{% endblock content %}
```

# 13. Enviar datos a un html
Suponiendo que ya se tiene el url entonces:
## 13.1) Crear la vista
```python
def task(request):
    tasks = Task.objects.filter( user = request.user, date_completed__isnull=True )
    tasks_complete = Task.objects.filter( user = request.user, date_completed__isnull=False )
    
    return render(request, 'tasks.html',{
        'tasks': tasks,
        'task_complete': tasks_complete
    })
```
## 13.2) Integrar los datos al html
```django
{% extends 'base.html' %}

{% block content %}

{% if tasks != null %}

    Todas tus tareas pendientes son:

    {% for task in tasks %}
    <section>
        <ul>
            <li>
                {{task.title}}
                {% if task.important %}
                ❗❗❗
                {% else %}
                🐢🐢🐢   
                {% endif %}
            </li>
            <h4>
                {{task.description}}
            </h4>
            <button>Actualizar</button>
        </ul>
    </section>
    {% endfor %}

{% endif %}

{% if tasks_complete != null %}

    Las tareas completadas son:
    {% for task in tasks_complete %}
    <section>
        <ul>
            <li>
                {{task.title}}
                {% if task.important %}
                ❗❗❗
                {% else %}
                🐢🐢🐢   
                {% endif %}
            </li>
            <h4>
                {{task.description}}
            </h4>
            <button>Actualizar</button>
        </ul>
    </section>
    {% endfor %}
{% endif %}

{% endblock content %}
```

## 13.3) Enviar parametros en el url
Hay que recordar que se puede solicitar variables en la url de la siguiente forma:
```python
...
    path('task/', views.task, name='tasks'),
    path('task/create/', views.task_create, name='create_task'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
    #  <tipo_variable: nombre_variable>
]
```
Asi que en la vista quedaria de la siguiente forma:
```python
from django.shortcuts import get_object_or_404

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'task.html', {'task': task})
```
Y para el template seria...
```django
{% extends 'base.html' %}

{% block content %}

<h1>{{task.title}}</h1>

<h2>{{task.description}}</h2>


{% endblock content %}
```