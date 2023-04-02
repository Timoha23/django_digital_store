## Digital Marketplace
![workflow](https://github.com/Timoha23/django_digital_store/actions/workflows/workflow.yml/badge.svg)
### Описание
---
Данный проект представляет собой онлайн-магазин электронной торговли, на котором любой пользователь может стать продавцом пройдя этапы модерации. 

### Используемые технологии
---
* Python 3.10.6;
* Django 4.1.7;
* Jquery 3.4.1;
* Bootstrap 5.1.1;
* Pillow 9.4.0.

### О проекте
---
В проекте представлены 4 роли пользователей:
<details> 
<summary>1. Анонимный пользователь ↓;</summary>
Возможности:

  ```
- Регистрация;
- Авторизация;
- Просмотр главной страницы;
- Просмотр всех товаров, которые прошли модерацию и имеют видимость=True;
- Просмотр всех магазинов, которые прошли модерацию;
- Просмотр отдельного продукта;
- Просмотр отзывов всего магазина;
- Просмотр профиля продавца;
- Просмотр всех товаров продавца;
- Просмотр всех магазинов продаца;
- Использовать поиск;
- Использовать поиск по категориям.

  ```
</details> 
<details>
<summary>2. Авторизованный пользователь (user) ↓;</summary>
Имеет все те же возможности, что и анонимный пользователь, без регистрации и авторизации, соответственно. Но к этому добавляются новые возможности:

  ```
- Выход из профиля;
- Открыть/редактировать/удалить магазин;
- Добавить/редактировать/удалить продукт;
- Добавить/удалить товар (например: ключ);
- Редактировать профиль:
- Добавлять товар в избранное;
- Просматривать избранные товары;
- Добавлять товар в корзину;
- Просматривать корзину;
- Изменять содержимое корзины внутри самой корзины;
- Оформлять покупку из корзины;
- Смотреть историю своих заказов;
- Оставлять отзывы на приобретенный товар.

  ```
</details>
<details>
<summary>3. Модерартор (moderator) ↓;</summary>
"Наследуемся" от авторизованного пользователя и расширяем функционал следующими возможностями:

  ```
- Имеет доступ к "Уголку модератора";
- Может принимать решения одобрить/отклонить", касательно новых/отредактированных магазинов/продуктов;
- Имеет доступ к просмотру всех магазинов имеющих статусы "одобрено/отклонено", и возможность изменять этот самый статус.

  ```
</details>
<details>
<summary>4. Администратор (admin) ↓;</summary>
Так же "наследуемся" от модератора и расширяем функционал следующим:

  ```
- Возможность выдать роль "Модератор", и забрать эту самую роль.

  ```
</details>

### Запуск проекта
---
1. Клонируем:
``` git clone https://github.com/Timoha23/django_digital_store.git ```
2. Устанавливаем venv:
``` python -m venv venv ```
3. Активируем venv:
``` source venv/Scripts/activate ```
4. Устанавливаем зависимости из requirements.txt
``` pip install -r requirements.txt ```
5. Переходим в папку с manage.py:
``` cd digital_store/ ```
6. Накатываем миграции:
``` python manage.py migrate ```
7. Запускаем проект(перед запуском настройте .env(пример ниже)):
``` python manage.py runserver ```
### Настройка .env
---
Создаем файл .env в главной директории и зполняем следующим образом:


    SECRET_KEY=YOUR_SECRET_KEY_DJANGO_PROJECT


Небольшая демонстрация добавления товара в корзину и в избранное:
![gif](https://user-images.githubusercontent.com/103051349/229347295-b8e85f41-adcd-490b-b6b0-6d8a25f30ca0.gif)
