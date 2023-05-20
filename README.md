# Сайт "Продуктовый помощник"
Проект Foodgram продуктовый помощник - платформа для публикации рецептов.

![Foodgram-project-react](https://github.com/niklukyan/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)


## Адрес развернутого приложения:

```
http://51.250.94.66/
```

## Описание проекта:
Проект Foodgram продуктовый помощник - платформа для публикации рецептов.
Cайт, на котором пользователи будут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволит пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

 * Реализован бекенд.
 * Фронтенд - одностраничное приложение на фреймворке React, которое взаимодействовует с API через удобный пользовательский интерфейс (разработан Яндекс.Практикум).

<div id="header" align="center">
  <img src="https://64.media.tumblr.com/11227c4f84cc97c20225955a615d2e5f/4f75de82137fa82f-c0/s2048x3072/7bb9e2ad562e498239e3fc5708954061248a1122.pnj"/>
</div>

#### Структура репозитория
 * В папке frontend находятся файлы, необходимые для сборки фронтенда приложения.
 * В папке infra — заготовка инфраструктуры проекта: конфигурационный файл nginx и docker-compose.yml.
 * В папке backend бэкенд продуктового помощника.
 * В папке data подготовлен список ингредиентов с единицами измерения. Список сохранён в форматах JSON и CSV. (Либо в файле фикстур)
 * В папке docs — файлы спецификации API.

#### Инфраструктура
 * Проект работает с СУБД PostgreSQL.
 * Проект запущен на сервере в трёх контейнерах: nginx, PostgreSQL и Django+Gunicorn. Контейнер с проектом обновляется на Docker Hub.
 * В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn.
 * Данные сохраняются в volumes.

#### Базовые модели проекта

**Рецепт**

 * Автор публикации (пользователь).
 * Название.
 * Картинка.
 * Текстовое описание.
 * Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
 * Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
 * Время приготовления в минутах.
 
<div id="header" align="center">
  <img src="https://64.media.tumblr.com/542095720bbfce6a1a72ae8edf33750c/2227aecc92389615-9e/s1280x1920/ea9068f46f1444f6df7edcc9cb5be673d72c24f5.pnj"/>
</div>

**Тег**

 * Название.
 * Цветовой HEX-код (например, #49B64E).
 * Slug.

**Ингредиент**

 * Название.
 * Количество.
 * Единицы измерения.

#### Сервисы и страницы проекта

<div id="header" align="center">
  <img src="https://64.media.tumblr.com/b5b44963ae72a953c18910c50eb21430/5fe11a1a7957f070-7d/s1280x1920/3bc03a75ddb1e61963779f89f664c043b08e9045.pnj"/>
</div>

#### Сервис "Список покупок"
Работа со списком покупок доступна авторизованным пользователям. Список покупок может просматривать только его владелец.

Сценарий поведения пользователя:
1.Пользователь отмечает один или несколько рецептов кликом по кнопке «Добавить в покупки».
2.Пользователь переходит на страницу Список покупок, там доступны все добавленные в список рецепты. Пользователь нажимает кнопку Скачать список и получает файл с суммированным перечнем и количеством необходимых ингредиентов для всех рецептов, сохранённых в «Списке покупок».
3.При необходимости пользователь может удалить рецепт из списка покупок.
Список покупок скачивается в формате .txt.
При скачивании списка покупок ингредиенты в результирующем списке не дублируются; если в двух рецептах есть сахар (в одном рецепте 5 г, в другом — 10 г), то в списке должен быть один пункт: Сахар — 15 г.

В результате список покупок может выглядеть так:
 * Фарш (баранина и говядина) (г) — 600
 * Сыр плавленый (г) — 200
 * Лук репчатый (г) — 50
 * Картофель (г) — 1000

----------

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
docker compose exec backend python manage.py collectstatic --no-input
```
Загружаем первоначальные данные(список ингредиентов и тегов) в БД при помощи фикстур
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
### Авторы
 
```
Никита Лукьянчук (8-918-261-01-04 nikluk@mail.ru)
``` 