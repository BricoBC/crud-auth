from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import TaskForm

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
                login(request, user)
                # Registrar en la cokie el request y el usuario.
                return redirect('/')
            except:
                error = 'Usuario ya existe'
        else:
            error = 'Las contraseñas no son iguales'
    
    # Al final retorna a la misma página y manda una cadena de texto
    return render(request, 'signup.html', {
    'forms': UserCreationForm,
    'error': error
    })

            
def home(request):
    return render(request, 'home.html')
        
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

def signout(request):
    logout(request)
    return redirect('/login')

def task_create(request):
    return render(request, 'create_task.html',{
        'form' : TaskForm
    })
    
def task(request):
    return render(request, 'tasks.html')