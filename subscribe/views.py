from django.shortcuts import render


from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from .forms_n import SubscriberForm
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)
@csrf_exempt
# def new(request):
#     if request.method == 'POST':
#         sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
#         sub.save()
#         message = Mail( from_email=settings.FROM_EMAIL,
#         to_emails=sub.email,
#         subject='Newsletter Confirmation',
#         html_content='Thank you for signing up for my email newsletter! \ Please complete the process by \ <a href="{}/confirm/?email={}&conf_num={}"> clicking here to \ confirm your registration</a>.'.format(request.build_absolute_uri('/confirm/'), sub.email, sub.conf_num))
#         sg = SendGridAPIClient('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')
#         response = sg.send(message)
#         return render(request, 'index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
#     else: return render(request, 'index.html', {'form_n': SubscriberForm()})

def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'delete_confirm.html', {'email': sub.email, 'action': 'confirmado'})
    else:
        return render(request, 'delete_confirm.html', {'email': sub.email , 'action': 'negado'})

def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'delete_confirm.html', {'email': sub.email, 'action': 'retirada na nossa Newsletter'})
    else:
        return render(request, 'delete_confirm.html', {'email': sub.email, 'action': 'negado'})