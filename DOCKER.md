# Dockerizing the expense_tracker backend

Build and start the app and database:

```bash
docker-compose up --build
```

Stop and remove containers and volumes:

```bash
docker-compose down -v
```

Run database migrations (after containers are running):

```bash
docker-compose exec backend flask db upgrade
```
