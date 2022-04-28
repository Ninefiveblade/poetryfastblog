### Проект написан c помощью Poetry ###

Установка OS Poetry:

```curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -```

### Установка зависимостей: ###

```poetry install```

### Использование в vscode ###
```poetry shell```
```code .```

### Запуск проекта: ###

```poetry shell```
```cd fastpoet```
```uvicorn main:app --reload```
