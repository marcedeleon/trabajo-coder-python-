from django.contrib import admin
from .models import task

# Register your models here.


class administrador_de_tarea(admin.ModelAdmin):
    readonly_fields = ("fecha_inicio",)


admin.site.register(task, administrador_de_tarea)
