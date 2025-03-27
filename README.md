# Taskiq_aiogram

## start worker
```shell
cd app/
taskiq worker tkq:broker --reload
```

## start bot
```shell
python bot.py 
```

## start scheduler

```shell
cd app/
taskiq scheduler tkq:scheduler

```

## Or docker-compose
```shell
docker compose up -d --build
```
