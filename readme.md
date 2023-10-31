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
# 8.1) Crear url 
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
# 8.2) Crear vista
```python
from django.contrib.auth import login, authenticate, logout
def signout(request):
    logout(request)
    return redirect('/login')
```
# 8.3)Crear plantilla base
La plantilla se integra con la de base.html

# 9. Modelos