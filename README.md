# Бронирование номера в отеле

Использовались **Django**, **Django REST Framework**, **Swagger** и **PostgreSQL**.

### Аутентификация
- Регистрация
- Логин через токен
- Только аутентицированные юзеры могут бронировать номер

### Комнаты
- Можно просмотреть комнаты без логина
- Их можно сфильтровать и сортировать через цену
- Также их вместимость
- Админы могут создавать, удалять, и отменять брони комнаты все привелегии

### Бронирование
- Доступные для брони комнаты можно фильтровать
- Забронировать комнату меж определенными датами
- Не будет двух броней в одну и туже комнату в выбранные даты
- Также даст цену смотря на количество дней
- Гости могут просмотреть свои брони и также отменить
- Админы имеют полный доступ к броням

### Документация
- Использвалась Swagger UI

## Стэк

- **Python 3.13**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **DRF Token Authentication**


## Как запустить код
```
git clone https://github.com/idon003/hotel_booking.git
cd hotel-booking

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

CREATE DATABASE hotel_db;
CREATE USER admin WITH PASSWORD 'admin'; --> или же можете изменить в settings.py
GRANT ALL PRIVILEGES ON DATABASE hotel_db TO admin;

python manage.py migrate makemigrations

python manage.py createsuperuser --> for admins
python manage.py runserver
```

## Скриншоты
Регистрация и логин
![](screenshots/Screenshot%202026-01-02%20at%2019.16.07.png)

Админ пейдж
![](screenshots/Screenshot%202026-01-03%20at%2011.32.38.png)
![](screenshots/Screenshot%202026-01-03%20at%2011.33.48.png)
После регистрации и логина дает токен ключь
![](screenshots/Screenshot%202026-01-03%20at%2011.36.41.png)
![](screenshots/Screenshot%202026-01-03%20at%2011.37.13.png)
Свободные комнаты для бронирование (не нужно аутентификация)
![](screenshots/Screenshot%202026-01-03%20at%2011.39.27.png)
Бронирование комнаты на опреденные даты (только через аутентификацию)
![](screenshots/Screenshot%202026-01-03%20at%2011.39.59.png)



