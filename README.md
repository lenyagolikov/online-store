# API сервис доставки
#### Скачивание репозитория, создание и активация виртуального окружения
    git clone https://github.com/lenyagolikov/online-store.git
    cd online-store && python3 -m venv env
    source env/bin/activate
#### Установка нужных зависимостей
    pip install -r requirements.txt
#### Создание базы данных в PostgreSQL: в примере ниже lenyagolikov - имя пользователя, 1234 - пароль, djcrm - название БД
    sudo -u root postgres psql
    create user lenyagolikov with password '1234';
    create database onlinestore;
    grant all privileges on database onlinestore to lenyagolikov;
#### Применение миграций и запуск сервера
    python3 manage.py migrate
    python3 manage.py runserver