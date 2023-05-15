# Сайт "Продуктовый помощник"
Проект Foodgram продуктовый помощник - платформа для публикации рецептов.

### Инструкция по запуску проекта локально в контейнерах

---------

1. Склонировать репозиторий на локальную машину
```
git clone git@github.com:NikLukyan/foodgram-project-react.git
```
2. В терминале из папки проекта перейти в папку infra
```
cd .\infra\
```
3. Выполнить команду по созданию образов и запуску контейнеров
```
docker compose up --build  
```
4. Инициализация БД и статики в контейнере
```
docker compose exec backend python manage.py migrate
```
Собираем статические файлы
```
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
Их общий пароль:
```
allTestUsersPASS$!
```
Загружаем первоначальные данные в БД при помощи фикстур
```
docker compose exec backend python manage.py loaddata --exclude auth.permission --exclude contenttypes fixtures.json
```
В фикстурах есть суперпользователь с почтой
```
nikluk@mail.ru
```
Пароль 
```
admin
```