from django import forms
from subscribe.models import Subscriber

class SubscriberForm(forms.Form):
    email = forms.EmailField(label='digite seu email:', max_length=100, required=True,
                                                           widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']

        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError('Esse email já esta cadastrado na Nossa Newsletter')
        return email
