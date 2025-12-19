# contact/views.py

from django.shortcuts import render, redirect
from django.views.generic import TemplateView 
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives # Para enviar correos con formato HTML
from django.template.loader import render_to_string # Para cargar plantillas de correo

from .forms import ContactForm 


# Vista basada en clase (CBV) para renderizar la página de contacto.
class ContactoPageView(TemplateView):
    template_name = 'contact/contacto.html'

    # Sobrescribimos get_context_data para pasar el formulario
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Creamos una instancia del formulario vacía
        context['form'] = ContactForm()
        return context


# Función para procesar el formulario (Envío de doble correo: Empresa y Cliente)
def contact_submit_view(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # 1. Obtener datos validados
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email'] # Email del cliente
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            
            # --- CONTEXTO PARA LAS PLANTILLAS DE CORREO ---
            context = {
                'nombre': nombre,
                'email': email,
                'asunto': asunto,
                'mensaje': mensaje,
                'subject': '' # Se actualizará en cada envío
            }
            
            try:
                # --- PASO 1: Enviar correo a la EMPRESA (INTERNO - HTML) ---
                context['subject'] = f"NUEVO MENSAJE DE CONTACTO: {asunto} (Desde: {email})"
                
                # Renderizar los cuerpos del correo
                html_body_internal = render_to_string('contact/email/internal_body.html', context)
                text_body_internal = render_to_string('contact/email/internal_body.txt', context)
                
                # Crear y enviar el objeto EmailMultiAlternatives
                msg_internal = EmailMultiAlternatives(
                    context['subject'],
                    text_body_internal, # Cuerpo de texto plano (fallback)
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.EMAIL_RECEIVER]
                )
                msg_internal.attach_alternative(html_body_internal, "text/html")
                msg_internal.send()
                
                
                # --- PASO 2: Enviar correo de CONFIRMACIÓN al CLIENTE (HTML) ---
                context['subject'] = "Confirmación: Hemos recibido tu mensaje en AGGREGATUM"
                
                # Renderizar los cuerpos del correo
                html_body_confirmation = render_to_string('contact/email/confirmation_body.html', context)
                text_body_confirmation = render_to_string('contact/email/confirmation_body.txt', context)

                # Crear y enviar el objeto EmailMultiAlternatives
                msg_confirmation = EmailMultiAlternatives(
                    context['subject'],
                    text_body_confirmation, # Cuerpo de texto plano (fallback)
                    settings.DEFAULT_FROM_EMAIL,
                    [email] # El correo del cliente
                )
                msg_confirmation.attach_alternative(html_body_confirmation, "text/html")
                msg_confirmation.send()
                
                
                messages.success(request, '¡Tu mensaje ha sido enviado con éxito! Te hemos enviado un correo de confirmación.')
                
                return redirect('contact:form') 

            except Exception as e:
                # Si falla el envío de correos (ej: credenciales SMTP inválidas)
                print(f"Error al enviar correo: {e}")
                messages.error(request, 'Hubo un error al enviar tu mensaje. Por favor, inténtalo de nuevo.')
                return render(request, 'contact/contacto.html', {'form': form})
        
        else:
            # Si el formulario no es válido (errores de validación)
            messages.error(request, 'Por favor, corrige los errores del formulario.')
            return render(request, 'contact/contacto.html', {'form': form})
            
    
    # Si alguien intenta acceder a la URL 'submit' por GET, lo redirigimos
    return redirect('contact:form')