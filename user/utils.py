from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings


from admin.celery import app
from user.models import UserProfile

import smtplib
import jwt


@app.task(bind=True, default_retry_delay=10 * 60)
def send_mail_to_user(self, data):
    try:
        send_mail(
            data['email_subject'],
            data['email_body'],
            "django.trade.app@gmail.com",
            [data['to_email']],
            fail_silently=False,
        )

    except smtplib.SMTPException as ex:
        self.retry(exc=ex)


def verify_user_email(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user = UserProfile.objects.get(id=payload['user_id'])

        if not user.verifyed_email:
            user.verifyed_email = True
            user.save()

        return Response({'email': "Email success confirmed."}, status=status.HTTP_200_OK)

    except jwt.ExpiredSignatureError:
        return Response({'error': "Activation Expired."}, status=status.HTTP_400_BAD_REQUEST)

    except jwt.exceptions.DecodeError:
        return Response({'error': "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
