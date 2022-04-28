# Проект написан на FastApi и помощью Poetry

Установить Poetry:
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
