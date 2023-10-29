# reg_centr_assignment

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=ffffff&color=043A6B)](https://www.django-rest-framework.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=ffffff&color=043A6B)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=ffffff&color=043A6B)](https://gunicorn.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=ffffff&color=043A6B)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=ffffff&color=043A6B)](https://www.docker.com/)


## Как запустить:
- скачайте репозиторий и скопируйте .env(можете настроить имя пользователя и пароль если необходимо или оставьте все как есть)
```
git clone git@github.com:pakodev28/reg_centr_assignment.git
```
```
cd reg_centr_assignment
```
```
cp .env.example .env
```
- Запустите контейнеры с помощью docker-compose
```
sudo docker-compose up -d
```

Теперь сервис доступен по этому [адресу](http://127.0.0.1/api/v1/recipes/)

### Пример запроса на создание рецепта
```
curl -X POST -H "Content-Type: application/json" -d '{
  "name": "Плов",
  "description": "Самый лучший на свете плов",
  "ingredients": [
    {
      "name": "мясо",
      "quantity": 800,
      "unit_of_measurement": "г"
    },
    {
      "name": "рис",
      "quantity": 400,
      "unit_of_measurement": "г"
    }
  ],
  "cooking_steps": [
    {
      "description": "Обжарить мясо",
      "time_in_minutes": 20
    },
    {
      "description": "Добавить рис",
      "time_in_minutes": 20
    }
  ]
}' http://127.0.0.1/api/v1/recipes/

```
### Пример запроса на обновление рецепта
```
curl -X PATCH -H "Content-Type: application/json" -d '{
  "name": "Новое название рецепта",
  "description": "Новое описание рецепта",
}' http://127.0.0.1/api/v1/recipes/<recipe_id>/

```