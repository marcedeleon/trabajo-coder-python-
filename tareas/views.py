from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from tareas.formularios import pedidos, UserEditForm
from .models import task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'home.html')


def registrar(request):
    if request.method == 'GET':
        return render(request, 'registrar.html', {'form': UserCreationForm})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tareas')
            except:
                return render(request, 'registrar.html', {'form': UserCreationForm, 'error': 'Usuario Ya Existe'})
        return render(request, 'registrar.html', {'form': UserCreationForm, 'error': 'Contraseñas no coinciden'})


@login_required
def tareas(request):
    tareas = task.objects.filter(
        usuario=request.user, fecha_fin__isnull=True)
    return render(request, 'tareas.html', {'tareas': tareas})


@login_required
def tareas_completas(request):
    tareas = task.objects.filter(
        usuario=request.user, fecha_fin__isnull=False).order_by('-fecha_fin')
    return render(request, 'tareas.html', {'tareas': tareas})


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'usuario incorrecto volve a intentarlo'})
        else:
            login(request, user)
            return redirect(tareas)


@login_required
def creando_tareas(request):
    if request.method == 'GET':
        return render(request, 'creando_tareas.html', {'form': pedidos})
    else:
        try:
            form = pedidos(request.POST)
            nuevo_pedido = form.save(commit=False)
            nuevo_pedido.usuario = request.user
            nuevo_pedido.save()
            print(nuevo_pedido.usuario)
            return redirect('tareas')
        except ValueError:
            return render(request, 'creando_tareas.html', {'form': pedidos, 'error': 'ingresa datos validos'})


@login_required
def detalletarea(request, tarea_id):
    if request.method == 'GET':
        tareas = get_object_or_404(task, pk=tarea_id)
        form = pedidos(instance=task)
        return render(request, 'detalletarea.html', {'tarea': tareas, 'form': form})
    else:
        try:
            tareas = get_object_or_404(task, pk=tarea_id)
            form = pedidos(request.POST, instance=tareas)
            form.save()
            return redirect('tareas')
        except:
            return render(request, 'detalletarea.html', {'tarea': tareas, 'form': form, 'error': "error intentando actualizar"})


@login_required
def tareacompletada(request, tarea_id):
    tarea = get_object_or_404(task, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.fecha_fin = timezone.now()
        tarea.save()
        return redirect('tareas')


@login_required
def borrar(request, tarea_id):
    tarea = get_object_or_404(task, pk=tarea_id, usuario=request.user)
    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'editar_perfil.html', {'form': form})
