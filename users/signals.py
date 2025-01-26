from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

User = get_user_model()


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    """ This signal send activation email when a user register """
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{
            settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        subject = 'Activate Your Account'
        message = f"Hi {instance.username},\n\nPlease activate your account by clicking the link below:\n{
            activation_url}\n\nThank you!"
        recipient_list = [instance.email]

        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
            print('Mail sent')
        except Exception as e:
            print(f"Failed to send activation email to {
                  instance.email}: {str(e)}")


@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    """ When a user register automatically assigned to User role """
    if created:
        user_group, created = Group.objects.get_or_create(name='User')
        instance.groups.add(user_group)
        instance.save()
