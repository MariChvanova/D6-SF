from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from news.models import Post
from .models import Subscriber

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == 'post_add':
        categories = instance.categories.all()
        for category in categories:
            subscribers = Subscriber.objects.filter(category=category).select_related('user')
            for subscriber in subscribers:
                subject = f'Новая статья в категории {category.name}'
                message = render_to_string('subscriptions/email/new_post_notification.html', {
                    'post': instance,
                    'category': category,
                    'user': subscriber.user,
                })
                send_mail(
                    subject=subject,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber.user.email],
                    html_message=message,
                    fail_silently=True,
                )