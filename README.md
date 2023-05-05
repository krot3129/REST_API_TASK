# REST_API_TASK


## Разработать сервис терминологии и REST API к нему.
Существуют сервисы, которые обмениваются между собой электронными документами. Электронный документ представляет собой структуру в формате
JSON.
Чтобы данные в полях таких документов были понятны принимающей системе и трактовались однозначно всеми участниками обмена, помимо структуры
документа, необходимо прийти к общему соглашению кодирования контекста данных.
Для этого потребуется независимый сервис терминологии, который хранит коды данных и их контекст. Проще говоря, это база данных справочников, с
кодами и значениями.

### Требования к окружению
  * Версия Python 3.10.6

### Разворачивание локального окружения разработки

### Установка необходимого ПО
* Создание виртуального окружения 
 ```commandline
  python3 -m venv название_виртуального_окружения
 ```
* Активация виртуального окружения
  - Для операционной системы Linux или macOS:
  ```commandline
  source название_виртуального_окружения/bin/activate
  ```
  - Для операционной системы Windows:
  ```commandline
  название_виртуального_окружения\Scripts\activate.bat
  ```
* Установка необходимый зависимостей:
```commandline
pip install -r requirements.txt
```
### Первый запуск приложения
* В директории проекта выполнить следующие действие
```commandline
python manage.py makemigrations
```
```commandline
python manage.py migrate
```
* Для установки фикструр (опционально) использовать следующию команду
```commandline
python manage.py loaddata fixtures/fixture.json
```
* Запуск сервера
```commandline
python manage.py runserver
```
### Для входа в Административную панель можно использовать следующие данные:
 - Login admin
 - password admin
### Примеры доступных API
* Список всех доступных справочников 
 - http://127.0.0.1:8000/refbooks/
 * Список справочников отфильтрованных по дате 
 - http://127.0.0.1:8000/refbooks/?date=2023-01-10 
 * Получение элементов справочника
 - http://127.0.0.1:8000/refbooks/1/elements/ 
 * Получение элементов справочника с версией 1.0
 - http://127.0.0.1:8000/refbooks/1/elements/?version=1.0 
 * Получение элементов справочника с версией 2.0
 - http://127.0.0.1:8000/refbooks/1/elements/?version=2.0 
 * проверка существования данного ссылочного элемента с кодом и значением.
   В конкретной версии справочника. 
 - http://127.0.0.1:8000/refbooks/1/check_element/?code=J00&value=()&version=1.0  
 - http://127.0.0.1:8000/refbooks/1/check_element/?code=J00&value=()&version=2.0 
 * Документация к API
 - http://127.0.0.1:8000/swagger/
 - http://127.0.0.1:8000/redoc/
 



