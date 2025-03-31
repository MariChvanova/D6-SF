from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Subscriber
from news.models import Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        action = request.POST.get('action')

        if category_id and action:
            try:
                category = Category.objects.get(id=category_id)

                if action == 'subscribe':
                    Subscriber.objects.get_or_create(user=request.user, category=category)
                    messages.success(request, f'Вы подписались на категорию "{category.name}"')
                elif action == 'unsubscribe':
                    Subscriber.objects.filter(user=request.user, category=category).delete()
                    messages.success(request, f'Вы отписались от категории "{category.name}"')

            except Category.DoesNotExist:
                messages.error(request, 'Категория не найдена')

        return redirect('subscriptions')

    categories = Category.objects.all()
    user_subscriptions = Subscriber.objects.filter(user=request.user).values_list('category_id', flat=True)

    return render(request, 'subscriptions/subscriptions.html', {
        'categories': categories,
        'user_subscriptions': user_subscriptions
    })