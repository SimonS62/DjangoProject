from django.shortcuts import render, redirect
from django.core.mail import send_mail


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        send_mail(
            'Сообщение с сайта',
            f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}',
            'from@example.com',  # Замените на ваш адрес отправителя
            ['to@example.com'],  # Замените на адрес получателя
            fail_silently=False,
        )
        return redirect('home')

    return render(request, 'catalog/contacts.html')


def home(request):
    return render(request, 'catalog/home.html')
