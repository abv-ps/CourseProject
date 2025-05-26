# Full Stack Microservice Architecture: Django + FastAPI + Kafka

This project demonstrates integration between a **FastAPI producer** and a **Django consumer** using Kafka for event-driven communication.

---

## Initial project setup

1. git clone https://github.com/abv-ps/CourseProject

    cd project-root
2. Create .env file in the root:

<pre>
DJANGO_SECRET_KEY=your_secret
DJANGO_DEBUG=True

DJANGO_POSTGRES_DB=django_db
DJANGO_POSTGRES_USER=django_user
DJANGO_POSTGRES_PASSWORD=django_password
DJANGO_POSTGRES_HOST=custom_postgres
DJANGO_POSTGRES_PORT=5432

RABBITMQ_USER=my_user 
RABBITMQ_PASSWORD=my_password
RABBITMQ_VHOST=my_vhost

CELERY_BROKER_URL=amqp://my_user:my_password@rabbitmq:5672/my_vhost
CELERY_RESULT_BACKEND=rpc://

CHAT_BROKER_URL=redis://redis:6379/1

FASTAPI_POSTGRES_DB=fastapi_db
FASTAPI_POSTGRES_USER=fastapi_user
FASTAPI_POSTGRES_PASSWORD=fastapi_password
FASTAPI_POSTGRES_HOST=postgres-fastapi
FASTAPI_POSTGRES_PORT=5433

KAFKA_BROKER=kafka:9092
KAFKA_TOPIC=tracking_topic
</pre>

3. Build and run containers:

<pre>
docker compose up --build
</pre>
## What Happens
- FastAPI sends events (create/update book or author) to Kafka.

- Django listens to the `tracking_topic` via Kafka Consumer and stores events in the database.

- Django handles Web UI and logs changes.

- Celery is used for async jobs (emails, periodic stats).

- Flower monitors Celery tasks.

- WebSocket support coming soon in FastAPI.
## Access Services

| **Service**           | **URL**                             | **Description**                                        |
|-----------------------|-------------------------------------|--------------------------------------------------------|
| Django Web App        | http://localhost:8000               | Main website (home, ads, profiles)                     |
| Django Admin Panel    | http://localhost:8000/admin         | Django administration dashboard                        |
| FastAPI App           | http://localhost:7000               | REST API for managing books and authors                |
| FastAPI Swagger       | http://localhost:7000/docs          | Swagger documentation for FastAPI                      |
| FastAPI ReDoc         | http://localhost:7000/redoc         | ReDoc documentation for FastAPI                        |
| RabbitMQ UI           | http://localhost:15672              | Message queue management (RabbitMQ)                    |
| Flower UI             | http://localhost:5555               | Celery task monitoring dashboard                       |
| PostgreSQL (Django)   | `localhost:5432`                    | PostgreSQL database used by the Django project         |
| PostgreSQL (FastAPI)  | `localhost:5433`                    | PostgreSQL database used by the FastAPI project        |
| Redis                 | `localhost:6379`                    | Redis cache / Celery broker                            |
| Kafka Broker          | `localhost:9092`, `localhost:9093`  | Kafka event/message broker                             |
| Zookeeper             | `localhost:2181`                    | Kafka coordination service                             |

**RabbitMQ login**:
<pre>
Username: my_user
Password: my_password
</pre>
## Django Web App Endpoints
| Category                | Method | Endpoint                         | Description                                                                  |
|-------------------------| ------ |----------------------------------|------------------------------------------------------------------------------|
| **Static Pages**        | GET    | `/`                              | Redirect to `/uk/home/` (*automatic i18n support)                                                    |
|                         | GET    | `/uk/home/`                      | Homepage                                                                     |
|                         | GET    | `/uk/home/about/`                | About Us page                                                                |
|                         | GET    | `/uk/home/contact/`              | Contact form                                                                 |
|                         | GET    | `/uk/home/services/`             | Services list                                                                |
| **Authentication**      | POST   | `/api/register/`                 | User registration                                                            |
|                         | POST   | `/api/token/`                    | Obtain JWT token                                                             |
|                         | POST   | `/api/token/refresh/`            | Refresh JWT token                                                            |
| **Books**               | GET    | `/api/books/`                    | List all books                                                               |
|                         | POST   | `/api/books/`                    | Create a book                                                                |
|                         | GET    | `/api/books/{id}/`               | Get book details                                                             |
|                         | PUT    | `/api/books/{id}/`               | Update book                                                                  |
|                         | DELETE | `/api/books/{id}/`               | Delete book                                                                  |
| **Admin Tokens**        | GET    | `/api/admin/tokens/`             | List all admin tokens                                                        |
|                         | GET    | `/api/admin/tokens/{user_id}/`   | Tokens for specific user                                                     |
|                         | DELETE | `/api/admin/tokens/delete/{id}/` | Delete a token                                                               |
| **API Documentation**   | GET    | `/api/docs/`                     | Swagger UI                                                                   |
|                         | GET    | `/api/redoc/`                    | ReDoc documentation                                                          |
| **Board**               | GET    | `/board/`                        | List ads                                                                     |
|                         | GET    | `/board/ad/{id}/`                | Ad details                                                                   |
|                         | GET    | `/board/profile/{id}/`           | User profile                                                                 |
|                         | POST   | `/board/profile/{id}/add_ad/`    | Add ad                                                                       |
|                         | POST   | `/board/profile/{id}/edit/`      | Edit profile                                                                 |
|                         | GET    | `/board/statistics/`             | Ad statistics                                                                |
| **Chat**                | GET    | `/chat/`                         | Simple web chat interface                                                    |
| **User Authentication** | —      | `/accounts/`                     | Managed via Django Allauth <br/>(registration, login, password change, etc.) |

## Django WebSocket Chat Endpoint

| Feature            | Endpoint                 | Description                                                                         |
| ------------------ | ------------------------ | ----------------------------------------------------------------------------------- |
| **WebSocket Chat** | `/ws/chat/<group_name>/` | Implemented via `Django Channels` and `AsyncJsonWebsocketConsumer` for group chat functionality |

Description:

- Connect via WebSocket with a specified 'group_name'.

- User authentication is automatic via Django session; anonymous users are rejected.

- Upon connection, the user is added to the given group (`group_name`) and the global group `GROUP_USER`. Superusers also join the `GROUP_ADMIN` group.

- A notification about the user joining is broadcasted to the group.

- Incoming JSON messages from clients are processed and broadcasted asynchronously using `AsyncJsonWebsocketConsumer`.

## FastAPI API Endpoints
| Category      | Method | Endpoint       | Description                  |
| ------------- | ------ | -------------- | ---------------------------- |
| **Books**     | GET    | `/books/`      | List all books               |
|               | POST   | `/books/`      | Create a book with authors   |
|               | PATCH  | `/books/{id}/` | Update book                  |
|               | DELETE | `/books/{id}/` | Delete book                  |
| **Authors**   | GET    | `/authors/`    | List all authors             |
|               | POST   | `/authors/`    | Create author                |

## Django Superuser (optional)
To manually create a Django admin user:
```
docker-compose exec web python manage.py shell
from django.contrib.auth.models import User
user = User.objects.create_user(
    username="admin",
    email="admin@example.com",
    password="your_password",
    is_staff=True,
    is_superuser=True
)
user.save()
```
## Media & Volumes
Uploaded media files will be stored in the media_data volume, mapped to /app/media/ in the Django container.
## Tech Stack
- Django (ASGI, PostgreSQL, Redis, Kafka consumer, Celery)

- FastAPI (PostgreSQL, Kafka producer, WebSocket)

- Kafka + Zookeeper

- RabbitMQ + Flower

- Docker Compose
