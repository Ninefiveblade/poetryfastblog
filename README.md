# Проект написан на FastApi с помощью Poetry

Установить [Poetry](https://python-poetry.org/):
```
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
```

Установить зависимости:
```
$ poetry install
```

Использовать Poetry в vscode:
```
$ poetry shell code .
```

Запуск проекта:
```
$ poetry run uvicorn fastpoet.main:app --reload
```
Документация по api:

```
http://127.0.0.1:8000/redoc/
```
