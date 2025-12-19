# core/views.py

from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "core/index.html"

class FabricaPageView(TemplateView):
    template_name = "core/fabrica.html"

class ProductosPageView(TemplateView):
    template_name = "core/productos.html"

class ProcesoPageView(TemplateView):
    template_name = "core/proceso.html"

class AcercaPageView(TemplateView):
    template_name = "core/acerca.html"

# La vista de Contacto irá en la app 'contacto'