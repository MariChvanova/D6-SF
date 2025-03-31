from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import Subscriber
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Send weekly newsletter to subscribers'

    def handle(self, *args, **options):
        last_week = timezone.now() - timedelta(days=7)

        for category in Category.objects.all():
            new_posts = Post.objects.filter(
                categories=category,
                created_at__gte=last_week
            ).order_by('-created_at')

            if new_posts.exists():
                subscribers = Subscriber.objects.filter(category=category).select_related('user')

                for subscriber in subscribers:
                    subject = f'Новые статьи в категории {category.name} за неделю'
                    message = render_to_string('subscriptions/email/weekly_newsletter.html', {
                        'category': category,
                        'posts': new_posts,
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

        self.stdout.write(self.style.SUCCESS('Weekly newsletter sent successfully'))