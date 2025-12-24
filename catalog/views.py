from django.shortcuts import render, redirect
# from django.core.mail import send_mail  # УДАЛЯЕМ ИМПОРТ

import json
from datetime import datetime


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Формируем словарь с данными
        data = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'phone': phone,
            'message': message
        }

        # Записываем данные в JSON-файл
        try:
            with open('contacts.json', 'a', encoding='utf-8') as f:  # Открываем файл в режиме добавления с кодировкой UTF-8
                json.dump(data, f, ensure_ascii=False)  # Отключаем экранирование ASCII
                f.write('\n')  # Разделяем записи новой строкой
        except Exception as e:
            # Обработка ошибок записи в файл
            print(f"Ошибка при записи в файл: {e}") # Логируем ошибку для отладки
            return render(request, 'catalog/contacts.html', {'error_message': 'Произошла ошибка при сохранении данных.'}) # Возвращаем ошибку на страницу

        # #  Старый код отправки email (УДАЛЕН)
        # send_mail(
        #     'Сообщение с сайта',
        #     f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}',
        #     'from@example.com',  # Замените на ваш адрес отправителя
        #     ['to@example.com'],  # Замените на адрес получателя
        #     fail_silently=False,
        # )

        return redirect('home') # Перенаправляем на главную страницу после успешной записи

    return render(request, 'catalog/contacts.html')


def home(request):
    return render(request, 'catalog/home.html')
