from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import TaskForm
from .models import Task
from django.utils import timezone

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
    
def task(request):
    tasks = Task.objects.filter( user = request.user, date_completed__isnull=True )
    tasks_complete = Task.objects.filter( user = request.user, date_completed__isnull=False )
    print('TAREAS INCOMPLETAS ')
    print(tasks)
    print('TAREAS COMPLETAS')
    print(tasks_complete)
    return render(request, 'tasks.html',{
        'tasks': tasks,
        'task_complete': tasks_complete
    })
    
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

def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.date_completed = timezone.now()
        task.save()
    return redirect('tasks')