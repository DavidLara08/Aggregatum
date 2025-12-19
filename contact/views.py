# contact/views.py

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string

from .forms import ContactForm
from .email_service import send_email


# Vista basada en clase (CBV) para renderizar la página de contacto
class ContactoPageView(TemplateView):
    template_name = 'contact/contacto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


# Función para procesar el formulario (envío de doble correo)
def contact_submit_view(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            # 1. Datos validados
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']

            # 2. Contexto común para los correos
            context = {
                'nombre': nombre,
                'email': email,
                'asunto': asunto,
                'mensaje': mensaje,
            }

            try:
                # =====================================================
                # PASO 1: CORREO INTERNO A LA EMPRESA
                # =====================================================
                subject_internal = (
                    f"NUEVO MENSAJE DE CONTACTO: {asunto} "
                    f"(Desde: {email})"
                )

                html_body_internal = render_to_string(
                    'contact/email/internal_body.html',
                    context
                )

                send_email(
                    subject=subject_internal,
                    html_content=html_body_internal,
                    to_email=settings.EMAIL_RECEIVER,
                    reply_to=email
                )

                # =====================================================
                # PASO 2: CORREO DE CONFIRMACIÓN AL CLIENTE
                # =====================================================
                subject_confirmation = (
                    "Confirmación: Hemos recibido tu mensaje en AGGREGATUM"
                )

                html_body_confirmation = render_to_string(
                    'contact/email/confirmation_body.html',
                    context
                )

                send_email(
                    subject=subject_confirmation,
                    html_content=html_body_confirmation,
                    to_email=email
                )

                messages.success(
                    request,
                    '¡Tu mensaje ha sido enviado con éxito! '
                    'Te hemos enviado un correo de confirmación.'
                )

                return redirect('contact:form')

            except Exception as e:
                print(f"Error al enviar correo con SendGrid: {e}")
                messages.error(
                    request,
                    'Hubo un error al enviar tu mensaje. '
                    'Por favor, inténtalo de nuevo.'
                )
                return render(
                    request,
                    'contact/contacto.html',
                    {'form': form}
                )

        else:
            messages.error(
                request,
                'Por favor, corrige los errores del formulario.'
            )
            return render(
                request,
                'contact/contacto.html',
                {'form': form}
            )

    # Si acceden por GET a la URL de submit
    return redirect('contact:form')
