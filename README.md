# FastAPI Wallet Service

REST API для работы с балансом кошельков.  
Сервис позволяет получать текущий баланс, пополнять кошелёк и списывать средства.

## Технологии

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- pytest
- asyncpg

## Запуск проекта

1. Скопировать `.env.example` в `.env` и при необходимости изменить значения.
2. В корне проекта выполнить команду:

```bash
docker compose up --build
```

## API

### Получить баланс кошелька

`GET /api/v1/wallets/{wallet_uuid}`

Возвращает текущий баланс кошелька.

### Выполнить операцию

`POST /api/v1/wallets/{wallet_uuid}/operation`

- `DEPOSIT` - положить средства
- `WITHDRAW` - снять средства

Пример запроса:

```json
{
  "operation_type": "DEPOSIT",
  "amount": 1000
}
```

Пример ответа:

```json
{
  "wallet_uuid": "550e8400-e29b-41d4-a716-446655440005",
  "balance": 1000
}
```

## Документация API

Swagger UI доступен по адресу:

`http://localhost:8000/docs`


## Конкурентность

При изменении баланса используется блокировка строки PostgreSQL (`SELECT ... FOR UPDATE`).
Это обеспечивает последовательную обработку параллельных операций над одним кошельком.

## Тесты
Перед первым запуском тестов необходимо создать отдельную тестовую базу данных `wallet_test_db`.

Таблицы в тестовой базе создаются и удаляются автоматически при запуске тестов.

Например, в PostgreSQL:

```sql
CREATE DATABASE wallet_test_db OWNER wallet_user;
```

Для запуска тестов выполнить:

```bash
python -m pytest
```
## Дополнительно

[Отзыв AI-ментора о процессе обучения](MENTOR_FEEDBACK.md)