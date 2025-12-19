# contact/urls.py

from django.urls import path
# ¡CORRECCIÓN AQUÍ! Eliminamos contact_success_view de la importación.
from .views import ContactoPageView
from . import views

app_name = 'contact'


urlpatterns = [
    # Muestra el formulario (GET)
    path('', ContactoPageView.as_view(), name='form'),

    # Procesa el formulario (POST)
    path('send/', views.contact_submit_view, name='submit'),
    
    # Asegúrate de que no haya ninguna ruta path('gracias/', ...) aquí.
]