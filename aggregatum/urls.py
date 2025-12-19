# aggregatum/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
# 1. Importar i18n_patterns
from django.conf.urls.i18n import i18n_patterns 

# Envolvemos las rutas de la aplicación con i18n_patterns
# Estas URLs ahora tendrán un prefijo de idioma (ej. /en/contacto/)
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    
    # Rutas de la aplicación principal (index, fabrica, etc.)
    path('', include('core.urls')), 
    
    # Rutas de la aplicación de contacto
    path('contacto/', include('contact.urls', namespace='contact')), 
)

# Las URLs que NO deben ser afectadas por el idioma (como herramientas de desarrollo)
# van fuera de i18n_patterns.
if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")), 
    ]