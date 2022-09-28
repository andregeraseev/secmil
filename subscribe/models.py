from django.db import models
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.http import HttpResponse

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    conf_num = models.CharField(max_length=15)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.email + " (" + ("não " if not self.confirmed else "") + "confirmado)"


class Newsletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=150)
    contents = models.FileField(upload_to='uploaded_newsletters/')


    def __str__(self):
        return self.subject + " " + self.created_at.strftime("%B %d, %Y")

    def send(self, request):
        contents = self.contents.read().decode('utf-8')
        subscribers = Subscriber.objects.filter(confirmed=True)

        for sub in subscribers:
            from_email = settings.FROM_EMAIL
            to_emails = sub.email
            subject = self.subject
            c = {
                'sub': sub,
                'domain': '127.0.0.1:8000',
                'site_name': 'Website',
                'protocol': 'http',
            }

            html_message = render_to_string('mail/footer_email.html', c)
            lala = render_to_string('mail/teste.html', c)
            # principal = render_to_string( contents, c )
            message = contents + lala
            # sg.send(message)
            try:
                send_mail(subject, message, from_email, [to_emails], html_message=contents+html_message)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
