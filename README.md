# Backend para el juego Catán - Grupo Catanes 

## Instalación

Descargar el repositorio con:

```
git clone https://gitlab.com/panicoro/catanes.git
```

Luego crear y levantar el [virtualenv](https://virtualenv.pypa.io/en/stable/), 
haciendo:

```
$ cd catanes/
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Tambien puede usarse [Pipenv](https://pipenv-es.readthedocs.io/es/latest/) para
crear el entorno virtual.

## Levantar servidor

Luego de activar el entorno virtual, ejecutar los siguientes comandos:

```
$ cd backend/
$ python manage.py makemigrations catan
$ python manage.py migrate
$ python manage.py runserver
```

## Testing

Para correr los test dentro de la backend y con el entorno virtual activado, 
hacer:

```
pytest --cov=catan --cov-report term-missing
```