# contact/forms.py

from django import forms

class ContactForm(forms.Form):
    # Aseguramos que los IDs y Placeholders sean los correctos
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre completo', 
            'id': 'id_nombre' # Esto asegura que el label apunte correctamente
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'tu@email.com', 
            'id': 'id_email'
        })
    )
    asunto = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': '¿En qué podemos ayudarte?', 
            'id': 'id_asunto'
        })
    )
    mensaje = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Cuéntanos más sobre tu proyecto o consulta...', 
            'rows': 6, 
            'id': 'id_mensaje'
        })
    )