# capa de vista/presentación

from django.shortcuts import redirect, render

from app.layers.transport import transport
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

def index_page(request):    
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.

def home(request):
    images = services.getAllImages(None)
    paginator = Paginator(images, 12)  #Cantidad de resultados
    page_number = request.GET.get('page', 1)  # Número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Página actual
    
    favourite_list = services.getAllFavourites(request)

    return render(request, 'home.html', { 'images': page_obj, 'paginator': paginator, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '') or request.GET.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        all_images = services.getAllImages(search_msg)
        paginator = Paginator(all_images, 12)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        return render(request, 'home.html', {'images': page_obj,'paginator': paginator,'search_msg': search_msg})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    if request.method == 'POST':
        services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    if request.method == 'POST':
        services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('index-page')