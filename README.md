## Сервис сбора пожертвований DonateNow

### 1. [Общая информация о проекте](#1)
### 2. [База данных и переменные окружения](#2)
### 3. [Команды для запуска](#3)
### 4. [Работа с API](#4)
### 5. [Использованные технологии](#5)
### 6. [Об авторе](#6)

---
### 1. Общая информация о проекте <a id=1></a>

Сервис сбора пожертвований DonateNow предоставляет пользователям следующие возможности:  
#### Неавторизованные пользователи:
  - могут зарегистрироваться
  - просматривать все проекты фонда
#### Зарегистрированные (авторизованные) пользователи:
  - могут делать то же, что и неавторизованные пользователи
  - осуществлять пожертвования на любую сумму и оставлять комментарии к ним
  - просматривать свои пожертвования
  - просматривать и редактировать свой аккаунт
#### Суперпользователи:
  - могут делать то же, что и обычные пользователи
  - создавать благотворительные проекты, редактировать их и удалять
  - просматривать все пожертвования сделанные в фонд
  - просматривать и редактировать аккаунты всех пользователей

---
### 2. База данных и переменные окружения <a id=2></a>

Проект использует базу данных SQLite.  
Для подключения и выполнения запросов к базе данных необходимо создать и заполнить файл ".env" с переменными окружения в корневой папке проекта.  
Пример:
```bash
APP_TITLE=Сервис сбора пожертвований DonateNow
DESCRIPTION=сервис сбора благотворительных взносов
DATABASE_URL=sqlite+aiosqlite:///./donatenow.db
SECRET=#Здесь напишите Ваш секретный код
```

---
### 3. Команды для запуска <a id=3></a>

Перед запуском необходимо склонировать проект:
```bash
HTTPS: git clone https://github.com/Invictus-7/donate_now
```

Cоздать и активировать виртуальное окружение:
```bash
python -m venv venv
```
```bash
Windows: source venv/Scripts/activate
```

Обновить pip и установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Выполнить миграции:
```bash
alembic upgrade head
```

Запустить проект:
```bash
uvicorn app.main:app
```

После запуска проект будет доступен по адресу [http://localhost:8000/](http://localhost:8000/)  
Документация по API проекта доступна можно по адресам:<a id=API></a>
  - Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
  - ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---
### 4. Работа с API <a id=4></a>

#### В проекте QRКот имеются следующие эндпоинты:
```
"/charity_project/"
"/charity_project/{project_id}/"
"/donation/"
"/donation/my"
"/auth/jwt/login"
"/auth/jwt/logout"
"/auth/register"
"/users/me"
"/users/{id}"
```

#### Примеры запросов:
- Получение всех проектов:
```
Method: GET
Endpoint: '/charity_project/'
```

- Создание благотворительного проекта:
```
Method: POST
Endpoint: '/charity_project/'
Payload:
{
    "name": "project_1",
    "description": "test project",
    "full_amount": 77077
}
```

- Внесение пожертвования:
```
Method: POST
Endpoint: '/donation/'
Payload:
{
  "full_amount": 55055,
  "comment": "for charity"
}
```

- Получить список всех своих пожертвований:
```
Method: GET
Endpoint: '/donation/my'
```

---
### 5. Использованные технологии <a id=5></a>

- [Python](https://www.python.org/)
- [FasAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

---
### 6. Об авторе <a id=6></a>
- [Кирилл Резник](https://github.com/Invictus-7)
