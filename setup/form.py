from django import forms

class ContactForm(forms.Form):
    nome = forms.CharField()
    email = forms.EmailField()
    telefone = forms.CharField()
    assunto = forms.CharField()
    mensagem = forms.CharField(widget=forms.Textarea)