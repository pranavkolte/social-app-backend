```shell
python -m venv .venv
pip install -r requirements.txt
alembic upgrade head
uvicorn app:app --reload

```