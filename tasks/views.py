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
    