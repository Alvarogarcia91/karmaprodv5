from django.shortcuts import render
# from .forms import *

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
#from .forms import SignUpForm
#from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.template.loader import get_template
from django.template import loader
#from .models import Cantidadp
#from corrida.models import Corrida, ElementoCorrida
#from .forms import *


def index(request):
    return HttpResponse('INDEX Respuesta http: Hola')


def espumas(request):
    return HttpResponse('espumas Respuesta http: Hola')

def respuesta(request):
    return HttpResponse('Respuesta http: Hola')
