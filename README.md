# <i>Barter Platform
### Веб-приложение Django для обмена вещами между пользователями
### Воможности:
* Пользователи могут размещать объявления о товарах для обмена
* Просматривать чужие объявления
* Отправлять предложения на обмен
* Rest API для работы с объявлениями и обменными предложениями

### Документация АPI:
После запуска сервера для просмотра доступных эндпоинтов перейдите по ссылке: http://localhost:8000/redoc/

### Установка:
#### 1. Клонируйте репозиторий:
`git clone https://github.com/AlexandrPavlushenko/BarterPlatform.git`
#### 2. Создайте и активируйте виртуальное окружение:
bash<br>
`python -m venv venv`<br><br>
`source venv/bin/activate`     # Linux/Mac<br>
`venv\Scripts\activate`        # Windows
#### 3. Установите зависимости
bash<br>
`pip install -r requirements.txt`
#### 4. Настройте базу данных:
В сервисе используется PostgreSQL<br><br>
bash<br>
`python manage.py makemigrations`<br>
`python manage.py migrate`
#### 5. Настройте переменные окружения
Создайте файл `.env` с настройками согласно шаблону, находящимуся в файле `.env.example`

#### 6. Запустите сервер
`python manage.py runserver`<br><br>
Приложение будет доступно по адресу: http://localhost:8000/
### Зависимости
Можно посмотреть в файле `requirements.txt` в корне проекта
### Тесты
Код покрыт тестами на 93%<br>
Запустить тесты c отчетом о покрытии можно командой<br>
`pytest --cov`<br>
или тесты для отдельных приложений<br>
`pytest --cov=ads`
`pytest --cov=api`
`pytest --cov=users`<br>
Настройки конфигурации pytest находятся в файле `pytest.ini` в корне проекта






