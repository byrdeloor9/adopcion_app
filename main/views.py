import http
from turtle import ht
from django.shortcuts import render
from django.http import Http404

from .models import Mascota


def home(request):

    mascotas = Mascota.objects.all()

    return render(request, 'home.html',{
        'mascotas':mascotas,
    } )

def mascota_detalle(request, mascota_id):

    try:
        mascota = Mascota.objects.get(id=mascota_id)

    except Mascota.DoesNotExist:
        raise Http404('Mascota no encontrada')

    return render(request, 'mascota_detalle.html',{
        'mascota':mascota,
        
    })