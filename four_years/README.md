# Лучшее вложение четырех лет молодости

## Требования к окружению 

- Python 3.9

### Установка зависимостей

В главном каталоге с файлом `requirements.txt`:
````commandline
pip install -r requirements.txt
````

## Запуск

### Шаг 1 

Миграция базы данных. **Выполнять только один раз.**
В главном каталоге с файлом `requirements.txt`:

```commandline
python four_years/manage.py makemigrations main_app
python four_years/manage.py makemigrations
python four_years/manage.py migrate
```
### Шаг 2

**Создание суперадмина**

```commandline
python four_years/manage.py createsuperuser
```

Далее вводим электроную почту (любую), пароль (он не будет ввиден при наборе) и потверждение пароля. 

### Шаг 3 

**Запуск сервера.**

```commandline
python four_years/manage.py runserver
```

Django уведомит о запуске. Проект будет доступен по адресу `http://127.0.0.1:8000`

## Заполнения базы данных

Базу даных можно наполнить через панель администратора который доступен по адресу `http://127.0.0.1:8000/admin`, вводим электроную почту и пароль от суперпользователя. 
Выбрав таблицу из списка, можно создать новое поле через кнопку которая расположенна в верхнем правом углу. 
