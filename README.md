```shell
uvicorn app:app --reload

```
```shell
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
