# Социальная сеть Yatube для публикации личных дневников

---
###Описание проекта
---
Социальная сеть для авторов и подписчиков. Пользователи могут подписываться на избранных авторов, оставлять и удалять комментари к постам, оставлять новые посты на главной странице и в тематических группах, прикреплять изображения к публикуемым постам.

###Запуск сервера
---
Для MacOs и Linux вместо python использовать python3
1. Клонирование репозитория:
```
git clone https://github.com/Lalkasasinka/YaTube.git
```
2. Cоздать и активировать виртуальное окружение:
```
cd YaTube
python -m venv venv
```
Для Windows:
```
source venv/Scripts/activate
```
Для MacOs/Linux:
```
source venv/bin/activate
```
3. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Создать и запустить миграции
```
cd yatube/
python manage.py makemigrations
python manage.py migrate
```
5. Запустить сервер:
```
python manage.py runserver
``` 
> После выполнения вышеперечисленных инструкций проект доступен по адресу http://127.0.0.1:8000/

##Контакты
---
Синицын Иван
[telegram](https://t.me/sSinichka)
