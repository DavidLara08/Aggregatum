# core/urls.py

from django.urls import path
from .views import HomePageView, FabricaPageView, ProductosPageView, ProcesoPageView, AcercaPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('fabrica-de-software/', FabricaPageView.as_view(), name='fabrica'),
    path('productos/', ProductosPageView.as_view(), name='productos'),
    path('nuestro-proceso/', ProcesoPageView.as_view(), name='proceso'),
    path('acerca/', AcercaPageView.as_view(), name='acerca'),
]