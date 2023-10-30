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

## 2. Instalación
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

## 3. Crear el proyecto, la app y ejecutar el servidor.
### 3.1) Proyecto
El proyecto va a tener como nombre **_crud-auth_**
```python
django-admin startproject crud-auth .
```
### 3.2) App
La aplicación se va a llamar **_tasks_**
```python
pythn manage.py startapp tasks
```

### 3.3) Ejecutar el proyecto
```python
python manage.py runserver
```
## 4. Interfaz Registrarse
Cuando se crea la app hay que recordar que se tiene que vincualar con las app del proyecto, se abre la carpeta del proyecto y se va al archivo de **_settings.py_**, se busca el array con nombre de **INSTALLED_APPS** y se agrega al final la app que se hizo.
### 4.1) Crear base de datos
Para cuando se crea un nuevo modelo recordemos que se utiliza el siguiente comando:
```python
python manage.py makemigrations
```

Para crear todos los modelos es con el siguiente comando:
```python
python manage.py migrate
```

### 4.2) Crear url
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

### 4.3) Crear vista
```python
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
#Ésta clase nos entrega el forms para el usuario

def main(request):
    return HttpResponse('<h1>Inicio.</h1>')

def signup(request):
    return render(request, 'signup.html', {
        'forms': UserCreationForm 
    })
    
```

### 4.4) Crear plantilla para la vista
```html
<h1>Signup</h1>

<form action="" method="post">
    <!-- Llave de seguridad -->
    {% csrf_token %}

    <!-- Formulario -->
    {{ forms.as_p }}
</form>
```



