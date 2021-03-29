Требования:
1. Python 3
2. PostgreSQL
3. Django, DRF

Советуется использовать виртуальное окружение:
1. Создайте директорию для проекта
    
    mkdir project
    cd project/
2. Создайте виртуальное окружение в директории
    
    virtualenv env
3. Активируйте виртуальное окружение
    
    source env/bin/activate

Установка:
1. Скачайте репозиторий в папку с проектом

    git clone https://github.com/lenyagolikov/online-store
2. Установите зависимости:
    
    pip install -r requirements.txt
    
Установка базы данных:
1. Скачайте postgresql

    sudo apt-get install postgresql
2. Откройте консоль psql и задайте пароль админа в БД

    sudo -u postgres psql postgres

    \password postgres
3. Создайте и настройте пользователя (user_name - имя пользователя, password - пароль)

    create user user_name with password 'password';
    
    alter role user_name set client_encoding to 'utf8';
    
    alter role user_name set default_transaction_isolation to 'read committed';
    
    alter role user_name set timezone to 'UTC';
4. Создайте базу данных (db_name - название базы, user_name - имя пользователя)

    create database db_name owner user_name;

Соединение с базой данных:
1. Откройте файл settings.py в папке onlinestore и настройте конфигурацию (db_name - имя БД, user_name - имя пользователя, password - пароль пользователя):

Запуск сервиса:
1. Откройте файл settings.py в папке onlinestore и настройте конфигурацию для ALLOWED_HOSTS (domain - домен):

    ALLOWED_HOSTS = ['domain']
3. Находясь в корневом репозитории (где лежит manage.py), выполните:

    python3 manage.py migrate
2. Запустите проект:

    python3 manage.py runserver (по умолчанию: порт 8000, домен: 127.0.0.1)
    
    или явно укажите домен и порт: python3 manage.py runserver <domain>:<port>
    

