from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .form import ContactForm
from django.template.loader import render_to_string
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from subscribe.models import Subscriber
from subscribe import forms_n
from subscribe.forms_n import SubscriberForm

import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt

def index(request):


    if request.method == 'POST' and 'email_s' in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["assunto"]
            from_email = form.cleaned_data["email"]
            message = form.cleaned_data['mensagem']
            nome = form.cleaned_data['nome']
            telefone = form.cleaned_data['telefone']
            mensagem = "nome: " + nome + '\n' + "email: " + from_email + '\n' + "telefone :" + telefone + '\n' + message
            try:
                send_mail(subject, mensagem, from_email, ["xflavors@gmail.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return render(request, 'index.html', { 'nome': nome, 'action': 'recebemos seu email', 'form_n': SubscriberForm(),'form' : ContactForm(request.POST) })

    if request.method == 'POST' and 'newsletter' in request.POST:
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        if Subscriber.objects.filter(email=request.POST['email']).exists():
            return render(request, 'index.html',
                          {'email': sub.email, 'action': 'cadastrado no nosso sistema anteriormente', 'form_n': SubscriberForm(),
                           'form': ContactForm(request.POST)})

        else:
            sub.save()


            from_email = 'ageraseev@gmail.com'
            to_emails = request.POST['email']
            subject = 'Confirmação Newsletter Secmil'
            message = 'mail/inscricao.html'
            c = {
                'sub' : sub,
                'domain': '127.0.0.1:8000',
                'site_name': 'Website',
                'protocol': 'http',
            }
            email = render_to_string(message, c)
            html_message = render_to_string('mail/confima_inscricao.html', c)
            # sg = SendGridAPIClient('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')
            # print(message, "MESSAGE")
            # response = sg.send(message)

            try:
                send_mail(subject, email, from_email, [to_emails],html_message=html_message)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")

            return render(request, 'index.html', {'email': sub.email, 'action': 'adicionado, confira seu email', 'form_n': SubscriberForm(),'form' : ContactForm(request.POST) })



    if request.method == "GET":
        form = ContactForm()
        form_n = SubscriberForm()

        data= {
            "form": form,
            'form_n': form_n

        }

        return render(request, "index.html", data)




def successView(request):
    return HttpResponse("Success! Thank you for your message.")



